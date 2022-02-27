import 'package:flutter/cupertino.dart';
import 'package:provider/provider.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'dart:convert';
import 'package:tank_manager/model/shared.dart';
import 'package:tank_manager/model/tank.dart';

import 'package:tank_manager/view/home_page.dart';

saveObj1(tanksList) async {
  SharedPreferences prefs = await SharedPreferences.getInstance();
  prefs.setString('obj1', jsonEncode(tanksList));
}

getObj1(BuildContext context) async {
  SharedPreferences prefs = await SharedPreferences.getInstance();
  if (prefs.containsKey('obj1')) {
    String obj1 = prefs.getString('obj1')!;
    Provider.of<UI>(context, listen: false).tanksList =
        List<Tank>.from(jsonDecode(obj1).map((obj1) => Tank.fromJson(obj1)));
  }
}
