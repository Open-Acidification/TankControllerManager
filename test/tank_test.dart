import 'package:flutter_test/flutter_test.dart';
import 'package:tank_manager/model/tank.dart';
import 'dart:convert';

void main() {
  test('Tank set name/ip', () {
    final tank = Tank('tank_test', '192.168.0.1');

    expect(tank.name, 'tank_test');
    expect(tank.ip, '192.168.0.1');
  });

  test('Tank equivalence', () {
    final tank = Tank('tank_test', '192.168.0.1');
    final tank2 = Tank('tank_test', '192.168.0.1');
    final tank3 = Tank('tank', '192.168.0.1');

    expect(tank, tank2);
    expect(tank, isNot(tank3));
  });

  test('Tank ', () {
    dynamic tank = Tank('tank_test', '192.168.0.1');
    String jsonTank = jsonEncode(tank);
    expect(jsonTank, '{"name":"tank_test","ip":"192.168.0.1"}');

    tank = jsonDecode(jsonTank);
    expect(tank, {'name': 'tank_test', 'ip': '192.168.0.1'});
  });
}