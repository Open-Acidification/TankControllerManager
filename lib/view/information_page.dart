import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:tank_manager/model/app_data.dart';
import 'package:tank_manager/model/tc_interface.dart';

class Information extends StatelessWidget {
  const Information({
    Key? key,
    required this.context,
  }) : super(key: key);

  final BuildContext context;

  @override
  Widget build(BuildContext context) {
    var appData = AppData.instance;
    var tcInterface = TcInterface.instance;
    tcInterface.get(appData.currentTank.ip, 'current').then((value) {
      appData.information = value;
    });
    return Consumer<AppData>(
      builder: (context, appData, child) {
        return RichText(
          text: TextSpan(
            text: appData.information,
          ),
        );
      },
    );
  }
}
