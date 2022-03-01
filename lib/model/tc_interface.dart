import 'package:http/http.dart' as http;

abstract class TcInterface {
  //Future<String> send(var value);
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
    return 'pH=7.352   7.218\nT=10.99 C 11.00' +
        path.substring(path.length - 1);
  }

  Future<String> get(var value, var path) async {
    if (path == 'current') {
      return "IPAddress:172.27.5.173, MAC:90:A2:DA:FD:C2:38, FreeMemory:3519 bytes, GoogleSheetInterval:20, LogFile:, PHSlope:, Kp:-31072.0, Ki:0.0, Kd:0.0, PID:ON, TankID:99, Uptime:4d 5h 15m 58s, Version:21.09.1";
    }
    return 'pH=7.352   7.218\nT=10.99 C 11.00' + path;
  }
}

class TcRealInterface extends TcInterface {
  Future<String> get(var ip, var path) async {
    var uri = 'http://$ip/api/1/$path';
    final response = await http.get(Uri.parse(uri));
    final testString = response.body.toString().replaceAll("\r", '');
    return testString;
  }

  Future<String> post(var ip, var path) async {
    var uri = 'http://$ip/api/1/$path';
    final response = await http.post(Uri.parse(uri));
    final testString = response.body.toString().replaceAll("\r", '');

    return testString;
  }
}
