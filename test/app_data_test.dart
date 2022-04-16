import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:tank_manager/model/app_data.dart';
import 'package:tank_manager/model/tank.dart';

void main() {
  var appData = AppData.instance;
  test('App current index', () {
    expect(appData.currentIndex, 0);
    appData.currentIndex = 3;
    expect(appData.currentIndex, 3);
  });

  test('App tank list', () {
    expect(appData.tankList, []);
    appData.addTank(Tank('Tank', '192.168.0.1'));
    expect(appData.tankList[0], Tank('Tank', '192.168.0.1'));
  });

  test('App Tank current', () {
    appData.currentTank = Tank('Tank', '192.168.0.1');
    expect(appData.currentTank, Tank('Tank', '192.168.0.1'));
  });

  group(
    "Write/Read",
    () {
      test('App write tank list', () async {
        List<Tank> tankList = [Tank('Tank', '192.168.0.1')];
        appData.writeTankList(tankList);

        SharedPreferences prefs = await SharedPreferences.getInstance();
        expect(prefs.getString('obj1'), '[{"name":"Tank","ip":"192.168.0.1"}]');
      });

      test('App read tank list', () async {
        await appData.readTankList();
        expect(appData.tankList, [Tank('Tank', '192.168.0.1')]);
      });
    },
  );
}
