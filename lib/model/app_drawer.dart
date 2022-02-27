import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:tank_manager/model/shared.dart';
import 'package:tank_manager/model/preferences.dart';
import 'package:tank_manager/model/tank.dart';

import 'package:tank_manager/view/home_page.dart';

class AppDrawer extends StatelessWidget {
  const AppDrawer({
    Key? key,
    required this.context,
  }) : super(key: key);

  final BuildContext context;

  @override
  Widget build(BuildContext context) {
    final ipController = TextEditingController();
    final nameController = TextEditingController();
    List<Widget> result = <Widget>[];
    return Drawer(
      backgroundColor: Colors.grey.shade600,
      child: Consumer<UI>(
        builder: (context, ui, child) {
          getObj1(context);
          for (var each in ui.tanksList) {
            result.add(tile(each));
          }
          return ListView(
            padding: EdgeInsets.zero,
            children: [
              drawerHeader(context),
              ...result,
              field(nameController, 'Name', 'Tank 99'),
              field(ipController, 'IP', '000.000.000.000'),
              Align(
                  alignment: Alignment.topRight,
                  child: FloatingActionButton(
                    onPressed: () {
                      var newTank =
                          Tank(nameController.text, ipController.text);
                      ui.addTank(newTank);
                      print(ui.tanksList.toString());
                      saveObj1(ui.tanksList);

                      nameController.text = "";
                      ipController.text = "";
                    },
                    tooltip: 'Add Tank',
                    child: const Icon(Icons.add),
                  ))
            ],
          );
        },
      ),
    );
  }

  Widget drawerHeader(BuildContext context) {
    return Container(
      child: DrawerHeader(
        child: Image.asset(
          'lib/assets/oap.png',
        ),
      ),
      color: Colors.blue,
    );
  }

  Widget field(var controller, var label, var hint) {
    return TextField(
      controller: controller,
      style: const TextStyle(color: Colors.black),
      decoration: InputDecoration(
        border: const OutlineInputBorder(),
        labelText: label,
        fillColor: Colors.grey.shade100,
        filled: true,
        hintText: hint,
      ),
    );
  }

  Widget tile(var selected) {
    return Consumer<UI>(builder: (context, ui, child) {
      return ListTile(
        title: Text(
          selected.name,
          style: const TextStyle(color: Colors.white),
        ),
        onTap: () {
          ui.currentTank = selected;

          Navigator.pop(context);
        },
      );
    });
  }
}
