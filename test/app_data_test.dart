import 'dart:convert';

import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:tank_manager/model/app_data.dart';
import 'package:tank_manager/model/tank.dart';

void main() async {
  TestWidgetsFlutterBinding.ensureInitialized();
  SharedPreferences.setMockInitialValues({});
  var appData = AppData.instance;

  tearDown(() {
    // Reset so that we no longer have a tankList
    appData.tankList.clear();
  });

  test('App current index', () {
    expect(appData.currentIndex, 0);
    appData.currentIndex = 3;
    expect(appData.currentIndex, 3);
  });

  test('App add and set current tank list', () {
    expect(appData.tankList, []);
    appData.addTank(Tank('Tank', '192.168.0.1'));
    expect(appData.tankList[0], Tank('Tank', '192.168.0.1'));
    appData.currentTank = Tank('Tank', '192.168.0.1');
    expect(appData.currentTank, Tank('Tank', '192.168.0.1'));
  });

  test('App write tank list', () async {
    expect(appData.tankList, []);
    List<Tank> tankList = [Tank('Tank', '192.168.0.1')];
    appData.writeTankList(tankList);
    SharedPreferences prefs = await SharedPreferences.getInstance();
    expect(prefs.getString('obj1'), '[{"name":"Tank","ip":"192.168.0.1"}]');
  });

  test('App read tank list', () async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    List<Tank> tankList = [Tank('Tank', '192.168.0.2')];
    prefs.setString('obj1', jsonEncode(tankList));

    await appData.readTankList();
    expect(appData.tankList, [Tank('Tank', '192.168.0.2')]);
  });

  test('App delete tank list', () {
    appData.addTank(Tank('Tank', '192.168.0.1'));
    expect(appData.tankList[0], Tank('Tank', '192.168.0.1'));
    appData.removeTank(Tank('Tank', '192.168.0.1'));
    expect(appData.tankList, []);
  });
}
