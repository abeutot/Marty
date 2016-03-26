from marty.commands import Command
from marty.printer import printer


WELLKNOW_TREE_ATTR_ORDER = ('type', 'ref', 'filetype', 'mode', 'uid', 'gid',
                            'atime', 'mtime', 'ctime')


def tree_attr_sorter(value):
    value = value[0]
    try:
        first = WELLKNOW_TREE_ATTR_ORDER.index(value)
    except ValueError:
        first = float('inf')

    return (first, value)


class ShowTree(Command):

    """ Show details about a tree object.
    """

    help = 'Show details about a tree object'

    def prepare(self):
        self._aparser.add_argument('remote', nargs='?')
        self._aparser.add_argument('name')

    def run(self, args, config, storage, remotes):
        name = '%s/%s' % (args.remote, args.name) if args.remote else args.name
        tree = storage.get_tree(name)
        max_name = max(len(x) for x in tree.names())
        for name, details in sorted(tree.items()):
            fmt = '<color fg=green>%s</color>:<color fg=cyan>%s</color>'
            details_text = ' '.join(fmt % (k, v) for k, v in sorted(details.items(), key=tree_attr_sorter))
            printer.p('<b>{n}</b> {d}', n=name.ljust(max_name).decode('utf-8', 'replace'), d=details_text)


class ShowBackup(Command):

    """ Show details about a backup object.
    """

    help = 'Show details about a backup object'

    def prepare(self):
        self._aparser.add_argument('remote', nargs='?')
        self._aparser.add_argument('name')

    def run(self, args, config, storage, remotes):
        name = '%s/%s' % (args.remote, args.name) if args.remote else args.name
        backup = storage.get_backup(name)
        printer.p('<b>Date:</b> {s} -> {e} ({d})',
                  s=backup.start_date.format('DD/MM/YYYY HH:mm:ss'),
                  e=backup.end_date.format('DD/MM/YYYY HH:mm:ss'),
                  d=backup.duration)
        printer.p('<b>Root:</b> {r}', r=backup.root)
        if backup.parent:
            printer.p('<b>Parent:</b> {b}', b=backup.parent)
        printer.p()
        printer.p('-' * 80)
        printer.p()
        printer.table(backup.stats_table(), fixed_width=80, center=True)
        printer.p()
