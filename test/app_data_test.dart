import 'dart:convert';
import 'package:tank_manager/model/tc_interface.dart';

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:tank_manager/model/app_data.dart';
import 'package:tank_manager/model/tank.dart';
import 'package:mockito/mockito.dart';

class MockBuildContext extends Mock implements BuildContext {}

void main() async {
  TcInterface.useMock();
  TestWidgetsFlutterBinding.ensureInitialized();
  SharedPreferences.setMockInitialValues({});
  var appData = AppData.instance;

  tearDown(() {
    // Reset so that we no longer have objects in tankList
    appData.tankList.clear();
  });

  test('App current index', () {
    expect(appData.currentIndex, 0);
    appData.currentIndex = 3;
    expect(appData.currentIndex, 3);
  });

testWidgets('App Invalid IP', (WidgetTester tester) async {
  expect(appData.tankList, []);
  bool flag = false;
  try {
    await appData.addTank(Tank('Tank', '127.0.0.1'));
  } catch (e) {
    flag = true;
  }
  expect(flag, true);
});

  test('App add, set current, and delete tank list', () async {
    expect(appData.tankList, []);
    await appData.addTank(Tank('Tank', '192.168.0.1'));
    expect(appData.tankList[0], Tank('Tank', '192.168.0.1'));
    appData.currentTank = Tank('Tank', '192.168.0.1');
    expect(appData.currentTank, Tank('Tank', '192.168.0.1'));
    appData.removeTank(Tank('Tank', '192.168.0.1'));
    expect(appData.tankList, []);
  });

  test('App write tank list', () async {
    expect(appData.tankList, []);
    List<Tank> tankList = [Tank('Tank', '192.168.0.1')];
    await appData.writeTankList(tankList);
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

}
