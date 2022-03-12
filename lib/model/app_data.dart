import 'package:flutter/material.dart';
import 'package:tank_manager/model/tank.dart';
import 'package:tank_manager/model/tc_interface.dart';

class AppData with ChangeNotifier {
  dynamic _currentTank = Tank('', '');
  var _display = '';
  var _information = '';
  List<Tank> _tankList = [];
  int _currentIndex = 0;

  void updateDisplay() async {
    var tcInterface = TcInterface.instance;
    tcInterface.get(currentTank.ip, 'display').then((value) {
      display = value;
    });
  }

  set information(information) {
    _information = information;
    notifyListeners();
  }

  void addTank(tank) {
    _tankList.add(tank);
    notifyListeners();
  }

  set currentIndex(index) {
    _currentIndex = index;
    notifyListeners();
  }

  set tanksList(tanksList) {
    _tankList = tanksList;
    notifyListeners();
  }

  set display(text) {
    _display = text;
    notifyListeners();
  }

  set currentTank(newTank) {
    _currentTank = newTank;
    notifyListeners();
  }

  String get information => _information;
  int get currentIndex => _currentIndex;
  List<Tank> get tanksList => _tankList;
  dynamic get currentTank => _currentTank;
  String get display => _display;
}
