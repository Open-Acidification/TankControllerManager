import 'package:flutter_test/flutter_test.dart';
import 'package:tank_manager/model/app_data.dart';
import 'package:tank_manager/model/tank.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  var appData = AppData.instance;
  test('Preferences save tank list', () async {
    List<Tank> tankList = [
      Tank('Tank1', '1'),
      Tank('Tank2', '1'),
      Tank('Tank3', '1')
    ];
    appData.writeTankList(tankList);
    SharedPreferences prefs = await SharedPreferences.getInstance();
    expect(prefs.getString('obj1'),
        '[{"name":"Tank1","ip":"1"},{"name":"Tank2","ip":"1"},{"name":"Tank3","ip":"1"}]');
  });
}
