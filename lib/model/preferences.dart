import 'package:flutter/cupertino.dart';
import 'package:provider/provider.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'dart:convert';
import 'package:tank_manager/model/app_data.dart';
import 'package:tank_manager/model/tank.dart';

saveObj1(tankList) async {
  SharedPreferences prefs = await SharedPreferences.getInstance();
  prefs.setString('obj1', jsonEncode(tankList));
}

getObj1(BuildContext context) async {
  if (Provider.of<AppData>(context, listen: false).tankList.isNotEmpty) return;
  SharedPreferences prefs = await SharedPreferences.getInstance();
  if (prefs.containsKey('obj1')) {
    String obj1 = prefs.getString('obj1')!;
    Provider.of<AppData>(context, listen: false).tankList =
        List<Tank>.from(jsonDecode(obj1).map((obj1) => Tank.fromJson(obj1)));
  }
}
