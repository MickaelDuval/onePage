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

        # faut le chemin complet vers le rep
        self.jinja_loader = jinja2.ChoiceLoader([
            self.jinja_loader,
            # jinja2.FileSystemLoader(os.path.join(config.repInstall,"html"))
            jinja2.FileSystemLoader(os.path.join(config.repInstall, config.repHtmlTechnique))
            ])

        self.dicGeneral = {
            "lstCSS":[]
        }

        self.dicGeneral["lstCSS"].append("css/defautOnePage.css")

    def index(self):
        return flask.render_template("index.html", **self.dicGeneral)

    # def sav(self, k, v):
    #     if not flask.session.get("data"):
    #         flask.session["data"] = {}
    #     flask.session["data"][k] = v
    #     self.dic[k] = v
    #     # print(f"Sav : {k} = {flask.session['data'][k]}")

    def getUrl(self, prefixe, fic):
        return flask.url_for(prefixe, filename=fic)
        
    def getPage(self):
        # TODO: gérer page 500 ici
        idPage = flask.request.form.get('idPage')
        
        # pour pouvoir tester dans le code des pages : autrement il va relancer le hasard qui s'est déja résolu
        self.rechargement = False

        # initial : on tente de charger depuis la session
        if idPage in ('', '#', None):
            # try : 
            #     idPage = flask.session["idPage"]
            #     self.rechargement = True
            # except KeyError: 
            idPage = config.pageIndex
        else : 
            # ça me plait moyen ça
            flask.session["idPage"] = idPage
            # flask.session.permanent = True
        
        
        # print(f"getPage {idPage}")

        self.dicReponse = {
                "texte":"",
                "app":self,
                "idPage":idPage,
            }

        for k,v in self.dicGeneral.items():
            self.dicReponse[k] = v

        # if not flask.session.get("data"):
        #     flask.session["data"] = {}

        # # print(f"{len(flask.session['data'].items())} items dans l'data")
        # for k,v in flask.session["data"].items():
        #     # print(f"session -> dic : self.dic[{k}] = {v}")
        #     self.dicReponse[k] = v

        bBlocCode = False
        try : 
            with open(os.path.join(config.repPages, idPage + ".html"), "r", encoding="utf-8") as f : 
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

                    self.dicReponse["texte"] += f"{l.strip()}\n"

        
        except FileNotFoundError: 
            # erreur 404
            with open(os.path.join(config.repInstall, config.repHtmlTechnique, "404.html"), "r", encoding="utf-8") as f : 
                self.dicReponse["texte"] = f"{f.read()}"

        # ! IMPORTANT : ce code est ajouté à chaque réponse pour ajouter la gestion des clics sur liens
        self.dicReponse["texte"] += """
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

        pageTmp = jinja2.Template(self.dicReponse["texte"])
        return pageTmp.render(**self.dicReponse)

    def modeTest(self):
        self.run(
            host=config.hoteDebug,
            port=config.portDebug,
            debug=True)

application = OnePage()

if __name__ == "__main__":
    os.system(f"START http://{config.hoteDebug}:{config.portDebug}")
    application.modeTest()

