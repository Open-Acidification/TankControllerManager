import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';
import 'package:tank_manager/model/app_data.dart';
import 'package:tank_manager/model/tank.dart';
import 'package:tank_manager/model/tc_interface.dart';

class Display extends StatelessWidget {
  const Display({
    Key? key,
    required this.context,
  }) : super(key: key);

  final BuildContext context;

  @override
  Widget build(BuildContext context) {
    var tcInterface = TcInterface.instance;
    return Consumer<AppData>(
      builder: (context, appData, child) {
        return InkWell(
          splashColor: Colors.grey.shade300,
          onTap: () {
            if (appData.currentTank != Tank('', '')) {
              tcInterface.get(appData.currentTank.ip, 'display').then((value) {
                appData.display = value;
              });
            }
            // if (shared.currentTank != Tank('', '')) {
            //   tcInterface.get(shared.currentTank.ip, 'display').then((value) {
            //     String x = value;
            //   });
            // }
          },
          child: Container(
            margin: const EdgeInsets.only(top: 20, bottom: 20),
            decoration: BoxDecoration(
              borderRadius: const BorderRadius.all(Radius.circular(5)),
              color: Colors.grey.shade800,
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.5),
                  spreadRadius: 5,
                  blurRadius: 7,
                  offset: const Offset(0, 3),
                ),
              ],
            ),
            height: 75.0,
            width: 320,
            child: Consumer<AppData>(
              builder: (context, appData, child) {
                return Text(
                  appData.display,
                  textAlign: TextAlign.center,
                  style: GoogleFonts.vt323(
                    fontSize: 35,
                    color: Colors.white,
                    letterSpacing: 3,
                  ),
                );
              },
            ),
          ),
        );
      },
    );
  }
}
