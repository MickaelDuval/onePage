#! /usr/bin/python3
#coding:utf-8

################################################################################
#                                Mickaël DUVAL
#                                  13/11/2020
################################################################################

import config
import flask
import jinja2
import sys
import os

class OnePage(flask.Flask):
    def __init__(self):
        flask.Flask.__init__(self, __name__)
        self.secret_key = "NanMaisLàFautMettreUneVraieClefDeSecu"

        self.add_url_rule("/", "Accueil", self.index, methods=["GET"])
        self.add_url_rule("/getPage", "Renvoie la page", self.getPage, methods=["POST"])

        # faut le rep complet
        # self.jinja_loader = jinja2.ChoiceLoader([self.jinja_loader, jinja2.FileSystemLoader(['D:/prj/webaventure/html']),])

        self.jinja_loader = jinja2.ChoiceLoader([
            self.jinja_loader,
            jinja2.FileSystemLoader(os.path.join(config.repInstall,"html"))
            ])

        self.dicGeneral = {
            "lstCSS":[]
        }

        self.dicGeneral["lstCSS"].append("css/webaventure.css")

    def index(self):
        return flask.render_template("index.html", **self.dicGeneral)


    def sav(self, k, v):
        if not flask.session.get("data"):
            flask.session["data"] = {}
        flask.session["data"][k] = v
        self.dic[k] = v
        # print(f"Sav : {k} = {flask.session['data'][k]}")

    def mort(self):
        flask.session.clear()

    def getUrl(self, prefixe, fic):
        return flask.url_for(prefixe, filename=fic)
        
    def getPage(self):
        numPage = flask.request.form.get('numPage')

        # pour pouvoir tester dans le code des pages : autrement il va relancer le hasard qui s'est déja résolu
        self.rechargement = False

        # initial : on tente de charger depuis la session
        if numPage == "#":
            try : 
                numPage = flask.session["numPage"]
                self.rechargement = True
            except KeyError: 
                numPage = config.pageIndex
        else : 
            flask.session["numPage"] = numPage
            # flask.session.permanent = True
        
        # if not numPage:
        #     numPage = "01"

        self.dic = {
                "texte":"",
                "app":self,
            }

        for k,v in self.dicGeneral.items():
            self.dic[k] = v

        if not flask.session.get("data"):
            flask.session["data"] = {}

        # print(f"{len(flask.session['data'].items())} items dans l'data")
        for k,v in flask.session["data"].items():
            # print(f"session -> dic : self.dic[{k}] = {v}")
            self.dic[k] = v

        bBlocCode = False
        try : 
            with open(f"{config.repPages}/{numPage}.html", "r", encoding="utf-8") as f : 
                for l in f.readlines():
                    if not len(l):
                        continue

                    if l.startswith("#code"):
                        tmpCode = ""
                        bBlocCode = True
                        continue

                    if l.startswith("#/code"):
                        try : 
                            exec(tmpCode)   
                        except Exception as err:
                            typeException, oException, oTraceBack = sys.exc_info()
                            # line_number = c.tb_lineno  # <-- this gets me 123,  not 6
                                #                             Frame : {oTraceBack.tb_frame}<br />
                                # Ligne : {oTraceBack.tb_lineno}<br />
                                # Instruction : {oTraceBack.tb_lasti}<br />

                            self.dic["texte"] += f"""
                                <p class="erreur">Erreur {typeException.__name__} : {str(err)}</p>
                                """

                        bBlocCode = False
                        continue

                    if bBlocCode:
                        tmpCode += l
                        continue

                    self.dic["texte"] += f"{l.strip()}\n"

        
        except FileNotFoundError: 
            self.dic["texte"] = f"""
            <h1>Malheureusement...</h1>
            <p class="erreur">Hélas, pauvre Yorick, le fichier <span class="chance">{config.repPages}/{numPage}.html</span> n'existe pas...</p>
            <p><a id="_index_" class="choix">Retour à la première page</a></p>
            """

        self.dic["texte"] += """
        <script>
            $(function(){
                $("a[id],.choix").click(function(evt){
                    if(this.nodeName == "A"){
                        $(this).attr('href', 'javascript:void(0)');
                    }
                    getPage(evt.target.id);
                });
            });
        </script>
        """

        # if not flask.session.get("data"):
        #     flask.session["data"] = {}

        # # print(f"{len(flask.session['data'].items())} items dans l'data")
        # for k,v in flask.session["data"].items():
        #     # print(f"session -> dic : self.dic[{k}] = {v}")
        #     self.dic[k] = v

        pageTmp = jinja2.Template(self.dic["texte"])
        return pageTmp.render(**self.dic)
        # return flask.render_template(f"page.html", **self.dic)

    def modeTest(self):
        self.run(host="localhost",port=config.portDebug,debug=True)

application = OnePage()

if __name__ == "__main__":
    os.system(f"START http://localhost:{config.portDebug}")
    application.modeTest()

