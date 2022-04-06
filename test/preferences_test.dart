import 'package:flutter_test/flutter_test.dart';
import 'package:tank_manager/model/preferences.dart';
import 'package:tank_manager/model/tank.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  test('Preferences save tank list', () async {
    List<Tank> tankList = [
      Tank('Tank1', '1'),
      Tank('Tank2', '1'),
      Tank('Tank3', '1')
    ];
    saveObj1(tankList);

    SharedPreferences prefs = await SharedPreferences.getInstance();
    expect(prefs.getString('obj1'),
        '[{"name":"Tank1","ip":"1"},{"name":"Tank2","ip":"1"},{"name":"Tank3","ip":"1"}]');
  });
}
