import 'package:flutter_test/flutter_test.dart';
import 'package:tank_manager/model/app_data.dart';
import 'package:tank_manager/model/tank.dart';

void main() {
  test('App current index', () {
    AppData app = AppData();

    expect(app.currentIndex, 0);
    app.currentIndex = 3;
    expect(app.currentIndex, 3);
  });

  test('App tank list', () {
    AppData app = AppData();

    expect(app.tankList, []);
    app.addTank(Tank('Tank', '192.168.0.1'));
    expect(app.tankList[0], Tank('Tank', '192.168.0.1'));
  });

  test('Tank set name/ip', () {
    AppData app = AppData();

    expect(app.currentIndex, 0);
    app.currentIndex = 3;
    expect(app.currentIndex, 3);
  });

  test('Tank set name/ip', () {
    AppData app = AppData();

    expect(app.currentIndex, 0);
    app.currentIndex = 3;
    expect(app.currentIndex, 3);
  });

  test('Tank set name/ip', () {
    AppData app = AppData();

    expect(app.currentIndex, 0);
    app.currentIndex = 3;
    expect(app.currentIndex, 3);
  });
}
