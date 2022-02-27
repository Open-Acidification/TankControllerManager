import 'package:flutter/material.dart';
import 'package:tank_manager/model/tank.dart';

class SHARED with ChangeNotifier {
  dynamic _currentTank = Tank('', '');
  var _display = '';
  List<Tank> _tanksList = [];
  int _currentIndex = 0;
  String _text = "";

  set text(text) {
    _text = text;
    notifyListeners();
  }

  void addTank(tank) {
    _tanksList.add(tank);
    notifyListeners();
  }

  set currentIndex(index) {
    _currentIndex = index;
    notifyListeners();
  }

  set tanksList(tanksList) {
    _tanksList = tanksList;
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

  String get text => _text;
  int get currentIndex => _currentIndex;
  List<Tank> get tanksList => _tanksList;
  dynamic get currentTank => _currentTank;
  String get display => _display;
}
