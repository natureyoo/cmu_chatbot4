#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""
Talk with a model using a web UI.
"""
import sys
sys.path.append('/home/jayeon/Documents/code/ParlAI')

from http.server import BaseHTTPRequestHandler, HTTPServer
from parlai.scripts.interactive import setup_args
from parlai.core.agents import create_agent
from parlai.core.worlds import create_task
from typing import Dict, Any
import parlai.utils.logging as logging
import pdb
import json

HOST_NAME = 'localhost'
PORT = 8080

SHARED: Dict[Any, Any] = {}
STYLE_SHEET = "https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.4/css/bulma.css"
FONT_AWESOME = "https://use.fontawesome.com/releases/v5.3.1/js/all.js"
WEB_HTML = """
<html>
    <link rel="stylesheet" href={} />
    <script defer src={}></script>
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=Edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title> WE ARE TEAM 4 </title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.9.0/js/all.min.js"></script>
    </head>
    <body>
        <div class="columns" style="height: 100%">
            <div class="column is-narrow">
                <div class="box" style="width: 250px; font-family:Georgia; margin-left: 20px;margin-top: 20px">
                    <label class="label">WIKI Search Instructions</label>
                    <br>
                    <p class="subtitle">If you want to check some references in Wikipedia,
                    <br> please attach <strong>'wiki:'</strong> at the beginning of your query.
                    </p>
                    <br><code> ex) wiki:what is a chatbot?</code>
                    
                </div>
            </div>
            <div style="width: 60%; margin-left: 0px; margin-right: 0px">
                
                <div class="column is-full" sytle:"margin-left: 0px; margin-right: 0px" >
                
                <section class="hero is-info is-large has-background-light has-text-grey-dark" style="height: 100%; width: 100%">
                   
                    <div id="parent" class="hero-body" style="overflow: auto; height: calc(100% - 76px); padding-top: 1em; padding-bottom: 0;">
                        <article class="media">
                        <div class="media-content">
                        <div class="box" style="background-color: teal; color:white; font-family:Georgia;">
                            <div class="content">
                            <p>
                                <strong>TEAM 4's CHATBOT</strong>
                                <br>
                                Hi, please type a message for me.
                            </p>
                            </div>
                        </div>
                        </div>
                        </article>
                    </div>

                    <div class="box">
                    <div class="hero-foot column is-offset-1" style="height: 76px">
                    <form id = "interact">
                        <div class="field is-grouped">
                            <p class="control is-expanded">
                            <input class="input is-primary is-rounded" type="text" id="userIn" placeholder="Enter your message">
                            </p>
                            <p class="control">
                            <button id="respond" type="submit" class="button is-primary">
                                <i class='fas fa-paper-plane'></i> Submit
                            </button>
                            </p>
                            <p class="control">
                            <button id="restart" type="reset" class="button is-warning">
                                <i class='fas fa-redo-alt'></i> Restart
                            </button>
                            </p>
                        </div>
                    </form>
                    </div>
                    </div>
                </section>
                </div>
            </div>

            <div id="wiki" style="height: 100%; width:40%">
                <iframe id="wiki_frame" src="https://en.wikipedia.org/"  style="height: 100%; width:100%">
                </iframe>
            </div>
        </div>

        <script>
            function createChatRow(agent, text, date, resptime) {{
                
                var article = document.createElement("article");
                article.className = "media"

                var figure = document.createElement("figure");
                figure.className = "media-left";

                var span = document.createElement("span");
                span.className = "icon is-large";

                var icon = document.createElement("i");
                icon.className = "fas fas fa-2x" + (agent === "You" ? " fa-user " : agent === "Model" ? " fa-tree" : "");

                var media = document.createElement("div");
                media.className = "media-content";

                var content = document.createElement("div");
                content.className = "content";

                var box = document.createElement("div");
                box.className = "box";

                var para = document.createElement("p");
                var paraText = document.createTextNode(text);


                var dateText = document.createTextNode(date);
                var resptimeText = document.createTextNode(resptime);

                var strong = document.createElement("strong");
                strong.innerHTML = agent;

                var br = document.createElement("br");
                var br1 = document.createElement("br");
                
                var timestamp = document.createElement("center");
                timestamp.innerHTML = date;
                timestamp.style.textAlign = "right";
                timestamp.style.fontSize = "small";
                timestamp.style.color = "#b8b6b2";

                var resptimestamp = document.createElement("center");
                resptimestamp.innerHTML = resptime;
                resptimestamp.style.textAlign = "right";
                resptimestamp.style.fontSize = "small";
                resptimestamp.style.color = "#a3a29e";


                para.appendChild(strong);
                para.appendChild(br);
                para.appendChild(paraText);
                // para.appendChild(br1);
                para.appendChild(timestamp);

                para.appendChild(resptimestamp);

                //para.appendChild(dateText);
                content.appendChild(para);
                media.appendChild(content);

                span.appendChild(icon);
                figure.appendChild(span);

                if (agent !== "TEAM 4's CHATBOT") {{
                    article.appendChild(figure);
                }};

                article.appendChild(media);

                return article;
            }}
            function createWiki(text){{                
                var idx_wiki = text.indexOf("wiki:");
                if (idx_wiki != -1){{
                    document.getElementById("wiki_frame").src="https://en.wikipedia.org/wiki/Special:Search?search="+text.substring(5, text.length);
                }}
            }}
            
            function saveToFile_Chrome(fileName, content) {{
                var blob = new Blob([content], { type: 'text/plain' });
                objURL = window.URL.createObjectURL(blob);
                if (window.__Xr_objURL_forCreatingFile__) {
                    window.URL.revokeObjectURL(window.__Xr_objURL_forCreatingFile__);
                }
                window.__Xr_objURL_forCreatingFile__ = objURL;
                var a = document.createElement('a');
                a.download = fileName;
                a.href = objURL;
                a.click();
            }}

            document.getElementById("interact").addEventListener("submit", function(event){{
                event.preventDefault()
                var text = document.getElementById("userIn").value;
                document.getElementById('userIn').value = "";
                var user_date = new Date();
                
                

                fetch('/interact', {{
                    headers: {{
                        'Content-Type': 'application/json'
                    }},
                    method: 'POST',
                    body: text
                }}).then(response=>response.json()).then(data=>{{
                    var parDiv = document.getElementById("parent");

                    parDiv.append(createChatRow("You", text, user_date, ""));
                   //  saveToFile_Chrome('log.csv', "User1"+","+text+","+user_date+",");

                    // Change info for Model response
                    var model_date = new Date();
                    response_time = model_date.getTime()-user_date.getTime() 

                    parDiv.append(createChatRow("Model", data.text, model_date,"@ Response Time : " + response_time/1000));
                   //  saveToFile_Chrome('log.csv',"Model"+","+data.text+","+model_date+","+response_time/1000);


                   //  parDiv.append(createChatRow("Response time (sec)", response_time/1000," ", " "));
                    
                    parDiv.scrollTo(0, parDiv.scrollHeight);
                    createWiki(text)
                }})
            }});
            document.getElementById("interact").addEventListener("reset", function(event){{
                event.preventDefault()
                var text = document.getElementById("userIn").value;
                document.getElementById('userIn').value = "";

                fetch('/reset', {{
                    headers: {{
                        'Content-Type': 'application/json'
                    }},
                    method: 'POST',
                }}).then(response=>response.json()).then(data=>{{
                    var parDiv = document.getElementById("parent");

                    parDiv.innerHTML = '';

                    var box = document.createElement("div");
                    box.style.cssText = "background-color: teal; color:white; font-family:Georgia;";
                    
                    box.className = "box";

                    box.append(createChatRow("TEAM 4's CHATBOT", "Hi, please type a message for me.","",""));


                    parDiv.appendChild(box)

                    parDiv.scrollTo(0, parDiv.scrollHeight);
                }})
            }});
        </script>

    </body>
</html>
"""  # noqa: E501


class MyHandler(BaseHTTPRequestHandler):
    """
    Handle HTTP requests.
    """

    def _interactive_running(self, opt, reply_text):
        reply = {'episode_done': False, 'text': reply_text}
        SHARED['agent'].observe(reply)
        #pdb.set_trace()
        model_res = SHARED['agent'].act()
        return model_res

    def do_HEAD(self):
        """
        Handle HEAD requests.
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        """
        Handle POST request, especially replying to a chat message.
        """
        if self.path == '/interact':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            body_decode = body.decode('utf-8')

            if body_decode.startswith('wiki:'):
                model_response = self._interactive_running(
                    SHARED.get('opt'), body_decode[5:]
                )
            else:
                model_response = self._interactive_running(
                    SHARED.get('opt'), body_decode
                )

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            json_str = json.dumps(model_response)
            self.wfile.write(bytes(json_str, 'utf-8'))
        elif self.path == '/reset':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            SHARED['agent'].reset()
            self.wfile.write(bytes("{}", 'utf-8'))
        else:
            return self._respond({'status': 500})

    def do_GET(self):
        """
        Respond to GET request, especially the initial load.
        """
        paths = {
            '/': {'status': 200},
            '/favicon.ico': {'status': 202},  # Need for chrome
        }
        if self.path in paths:
            self._respond(paths[self.path])
        else:
            self._respond({'status': 500})

    def _handle_http(self, status_code, path, text=None):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        content = WEB_HTML.format(STYLE_SHEET, FONT_AWESOME)
        return bytes(content, 'UTF-8')

    def _respond(self, opts):
        response = self._handle_http(opts['status'], self.path)
        self.wfile.write(response)


def setup_interactive(shared):
    """
    Build and parse CLI opts.
    """
    parser = setup_args()
    parser.add_argument('--port', type=int, default=PORT, help='Port to listen on.')
    parser.add_argument(
        '--host',
        default=HOST_NAME,
        type=str,
        help='Host from which allow requests, use 0.0.0.0 to allow all IPs',
    )

    SHARED['opt'] = parser.parse_args(print_args=False)

    SHARED['opt']['task'] = 'parlai.agents.local_human.local_human:LocalHumanAgent'

    # Create model and assign it to the specified task
    agent = create_agent(SHARED.get('opt'), requireModelExists=True)
    SHARED['agent'] = agent
    SHARED['world'] = create_task(SHARED.get('opt'), SHARED['agent'])

    # show args after loading model
    parser.opt = agent.opt
    parser.print_args()
    return agent.opt


if __name__ == '__main__':
    opt = setup_interactive(SHARED)
    MyHandler.protocol_version = 'HTTP/1.0'
    httpd = HTTPServer((opt['host'], opt['port']), MyHandler)
    logging.info('http://{}:{}/'.format(opt['host'], opt['port']))

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
