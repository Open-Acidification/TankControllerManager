import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:tank_manager/model/tank.dart';
import 'package:tank_manager/model/tc_interface.dart';

class AppData with ChangeNotifier {
  static AppData? _instance;

  static get instance {
    _instance ??= AppData();
    return _instance;
  }

  dynamic _currentTank = Tank('', '');
  var _display = '';
  var _information = <String, dynamic>{};
  List<Tank> _tankList = [];
  int _currentIndex = 0;

  Future<void> readTankList() async {
    if (tankList.isNotEmpty) return;
    WidgetsFlutterBinding.ensureInitialized();
    SharedPreferences prefs = await SharedPreferences.getInstance();
    if (prefs.containsKey('obj1')) {
      String obj1 = prefs.getString('obj1')!;
      tankList =
          List<Tank>.from(jsonDecode(obj1).map((obj1) => Tank.fromJson(obj1)));
    }
  }

  Future<void> writeTankList(tankList) async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    prefs.setString('obj1', jsonEncode(tankList));
  }

  Future<void> updateDisplay() async {
    var tcInterface = TcInterface.instance;
    tcInterface.get(currentTank.ip, 'display').then((value) {
      display = value;
    });
  }

  Future<void> updateInformation() async {
    var tcInterface = TcInterface.instance;
    var value = await tcInterface.get(currentTank.ip, 'current');
    _information = jsonDecode(value);
    notifyListeners();
  }

  void addTank(tank) {
    _tankList.add(tank);
    notifyListeners();
    writeTankList(tankList);
  }

  set currentIndex(index) {
    _currentIndex = index;
    notifyListeners();
  }

  set tankList(tankList) {
    _tankList = tankList;
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

  Map<String, dynamic> get information => _information;
  int get currentIndex => _currentIndex;
  List<Tank> get tankList => _tankList;
  dynamic get currentTank => _currentTank;
  String get display => _display;
}
