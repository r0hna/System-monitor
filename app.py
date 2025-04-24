from flask import Flask, jsonify, request, render_template

monitorApp = Flask(__name__)
#monitorApp.config['SECRET_KEY'] = 'IUIU&#IU$U@#$8887$*&848748748783u45rbhuhbghyujhbgYUJHY7uHY&Uy&*iYUiJHyuIuII'

@monitorApp.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@monitorApp.route('/', methods=["GET"])
def home():
    return jsonify({"Server": "It is running."})

@monitorApp.route('/rule/get/{rule_name}', methods=["GET"])
def get_a_rule():
    return jsonify({"msg": "Server is up"})  

@monitorApp.route('/rule/get/all', methods=["GET"])
def rule_get_all():
    return jsonify({"msg": "Server is up"})


@monitorApp.route('/rule/custom/add', methods=["POST"])
def custom_rule():
    if request.method == "POST":
        return jsonify({"It is working"})
    
    return jsonify({"Server": "This method is not allowed!"})

@monitorApp.route('/system/health', methods=["GET"])
def health_status():
    if request.method == "GET":
        from agents.system_health import get_system_health
        data = get_system_health()
        data.headers.add('Access-Control-Allow-Origin', '*')
        return data
    return jsonify({"Server":"This method is not allowed"})


@monitorApp.route('/hostscan', methods=["GET"])
def host_scan():
    from agents.host_scan import live_hosts
    return jsonify(live_hosts())

@monitorApp.route('/portscan', methods=["GET"])
def port_scan():
    if request.method == 'GET':
        ip = request.args.get('ip')
        if  ip:
            from agents.port_scan import scan
            return jsonify(scan())
        return jsonify({"Server": "Parameter value is not found or data type not supported!", "Recommendation": "Check out the API documentation!"})
    return jsonify({"Server": "This mehtod is not allowed"})

    

@monitorApp.route('/usbdevices', methods=["GET"])
def usbdevices():
    from agents.usb_monitor import get_usb_devices
    return jsonify(get_usb_devices())

#------------------ logs ------------------------
@monitorApp.route('/log/system', methods=["GET"])
def system_log():
    from agents.logs import read_event_logs
    all_logs = read_event_logs('system')
    return jsonify(all_logs)

@monitorApp.route('/log/application', methods=["GET"])
def application_log():
    from agents.logs import read_event_logs
    all_logs = read_event_logs('application')
    return jsonify(all_logs)

@monitorApp.route('/log/security', methods=["GET"])
def security_log():
    from agents.logs import read_event_logs
    all_logs = read_event_logs('security')
    return jsonify(all_logs)

@monitorApp.route('/log/setup', methods=["GET"])
def setup_log():
    from agents.logs import read_event_logs
    all_logs = read_event_logs('setup')
    return jsonify(all_logs)

#------------------------------------------------

@monitorApp.route('/packet', methods=["GET"])
def get_packet():
    if request.method == 'GET':
        qty = request.args.get('q')
        type_qty = type(qty).__name__
        if  type_qty == 'str':
            from agents.packets_analysis import capture_network_traffic
            packet = capture_network_traffic(packet_count=int(qty))
            return jsonify(packet)
        return jsonify({"Server": "Parameter value is not found or data type not supported!", "Recommendation": "Check out the API documentation!"})
    return jsonify({"Server": "This mehtod is not allowed"})

@monitorApp.route('/packets', methods=["GET"])
def packets():
    from agents.packets_analysis import capture_network_traffic
    all_packets = capture_network_traffic(packet_count=100)
    return jsonify(all_packets)

@monitorApp.route('/endpoints', methods=["GET"])
def endpoints():
    return render_template('endpoints.html')


if __name__ == "__main__":
    monitorApp.run(debug=True, host='0.0.0.0')
    
