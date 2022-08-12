import 'package:http/http.dart' as http;

abstract class TcInterface {
  static TcInterface? _instance;

  static get instance {
    _instance ??= TcRealInterface();
    return _instance;
  }

  static void useMock() {
    _instance = TcMockInterface();
  }
}

class TcMockInterface extends TcInterface {
  Future<String> post(var value, String path) async {
    return 'pH=7.352   7.218\nT=10.99 C 11.00${path.substring(path.length - 1)}';
  }

  Future<String> get(var value, var path) async {
    if (path == 'current') {
      return '{"IPAddress":"172.27.5.150","MAC":"90:A2:DA:0F:45:C0","FreeMemory":"3791 bytes","GoogleSheetInterval":10,"LogFile":"20220722.csv","PHSlope":"","Kp":9000.4,"Ki":0.0,"Kd":0.0,"PID":"ON","TankID":3,"Uptime":"0d 0h 1m 7s","Version":"22.04.1"}';
    }
    return 'pH=7.352   7.218\nT=10.99 C 11.00$path';
  }
}

class TcRealInterface extends TcInterface {
  Future<String> get(var ip, var path) async {
    var uri = 'http://$ip/api/1/$path';
    final response = await http.get(Uri.parse(uri));
    final subString = response.body.toString().replaceAll("\r", '');
    return subString;
  }

  Future<String> post(var ip, var path) async {
    var uri = 'http://$ip/api/1/$path';
    final response = await http.post(Uri.parse(uri));
    final subString = response.body.toString().replaceAll("\r", '');

    return subString;
  }
}
