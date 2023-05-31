from subprocess import Popen, PIPE, STDOUT
import functools


def output(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        r = f(*args, **kwargs)
        if r is not None and len(r) > 0:
            print r
            return
        print(f.__doc__)

    return wrapper


class CliApp:

    def __init__(self):
        pass

    def shell_run(self, cmd, **args):
        p = Popen(cmd, stdout=PIPE,
                  stderr=STDOUT, shell=True)
        results = []
        silent = 'silent' in args and args['silent'] == True
        while True:
            line = p.stdout.readline().strip()
            if not line:
                break
            results.append(line)
            if not silent:
                print(line)
        p.communicate()
        return (results, p.returncode)

    @output
    def print_helper(self, args):
        if len(args) > 0:
            cmd = args[0]
            if not self.validate_cmd(cmd):
                return 'do not make things up man. I cannot help you on {}'.format(cmd)
            return '{} : {}'.format(cmd, getattr(self, 'do_{}'.format(cmd)).__doc__)
        outputs = list()
        for f in dir(self):
            if f.startswith('do_'):
                outputs.append(f[3:])
        if len(outputs) > 0:
            return 'man, you gotta choose from following: {}'.format(outputs)
        return 'no help contents available'

    @output
    def print_valid_options(self):
        outputs = list()
        if 'urls' in dir(self):
            outputs.append('valid wheres: {}'.format(self.urls.keys()))
        dos = []
        for f in dir(self):
            if f.startswith('do_'):
                dos.append(f[3:])
        outputs.append('valid whats: {}'.format(dos))
        return '\n'.join(outputs)

    def validate_cmd(self, cmd):
        return 'do_%s' % (cmd) in dir(self)

    def parse_args(self, args):
        d = {}
        for a in args:
            parts = a.split('=', 1)
            if len(parts) > 1:
                d[parts[0]] = parts[1]
        return d

    def run(self, args):
        if len(args) < 1:
            self.print_valid_options()
            return 1
        cmd = args[0]
        if cmd == 'help':
            self.print_helper(args[1:])
            return 0
        try:
            if not self.validate_cmd(cmd):
                self.print_valid_options()
                return 1
            kwargs = self.parse_args(args[1:])
            getattr(self, 'do_%s' % (cmd))(**kwargs)
        except Exception as e:
            print(e)
            return 1
