import genshi.template
import Bcfg2.Server.Lint

class Genshi(Bcfg2.Server.Lint.ServerPlugin):
    """ Check Genshi templates for syntax errors """
    def Run(self):
        """ run plugin """
        loader = genshi.template.TemplateLoader()
        for plugin in ['Cfg', 'TGenshi']:
            if plugin in self.core.plugins:
                self.check_files(self.core.plugins[plugin].entries,
                                 loader=loader)

    @classmethod
    def Errors(cls):
        return {"genshi-syntax-error":"error"}

    def check_files(self, entries, loader=None):
        if loader is None:
            loader = genshi.template.TemplateLoader()

        for eset in entries.values():
            for fname, sdata in list(eset.entries.items()):
                if (self.HandlesFile(fname) and
                    (fname.endswith(".genshi") or fname.endswith(".newtxt"))):
                    try:
                        loader.load(sdata.name,
                                    cls=genshi.template.NewTextTemplate)
                    except genshi.template.TemplateSyntaxError:
                        err = sys.exc_info()[1]
                        self.LintError("genshi-syntax-error",
                                       "Genshi syntax error: %s" % err)
