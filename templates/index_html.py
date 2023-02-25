# Autogenerated file
def render(configjson):
    yield """
<html>
    <body>
        <h1>Water Softener sensor config</h1>
        
        <p>Sample config:</p>
        
        <pre>
        <code>
        """
    yield """{
            \"wifissid\" : \"[wifi SSID name]\",
            \"wifipassword\" : \"[wifi password]\",
            \"mqtt_server\" : \"[IP address of MQTT server]\",
            \"mqttusername\" : \"[username for MQTT server]\",
            \"mqttpassword\" : \"[password for MQTT server]\",
            \"secondsbetweenchecking\" : [how many seconds to wait after each sensor check]
        }
        </code>
        </pre>
        
        <form method=\"post\">
            <label for=\"password\">Password:</label>
            <input type=\"password\" name=\"password\" id=\"password\" placeholder=\"Password\" />
            <br />
            <br />
            <label for=\"password\">JSON Config File:</label>
            <br />
            <textarea id=\"configjson\" name=\"configjson\" rows=\"10\" cols=\"80\">"""
    yield str(configjson)
    yield """</textarea>
            <br />
            <input type=\"submit\" value=\"Save\" />
        </form>
    </body>
    
    <img src=\"/images/softener.jpg\" alt=\"Use rust fighting salt!\" />
    <img src=\"/images/salt.jpg\" alt=\"Use rust fighting salt!\" />
</html>
"""
