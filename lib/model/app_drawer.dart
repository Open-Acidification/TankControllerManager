import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:tank_manager/model/shared.dart';
import 'package:tank_manager/model/preferences.dart';
import 'package:tank_manager/model/tank.dart';
import 'package:tank_manager/model/tc_interface.dart';

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
      child: Consumer<SHARED>(
        builder: (context, shared, child) {
          getObj1(context);
          for (var each in shared.tanksList) {
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
                    var newTank = Tank(nameController.text, ipController.text);
                    shared.addTank(newTank);
                    saveObj1(shared.tanksList);
                  },
                  tooltip: 'Add Tank',
                  child: const Icon(Icons.add),
                ),
              ),
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
    var tcInterface = TcRealInterface();
    return Consumer<SHARED>(builder: (context, shared, child) {
      return ListTile(
        title: Text(
          selected.name,
          style: const TextStyle(color: Colors.white),
        ),
        onTap: () {
          shared.currentTank = selected;
          tcInterface
              .get(shared.currentTank.ip, 'display')
              .then((value) => shared.display = value);
          tcInterface
              .get(shared.currentTank.ip, 'current')
              .then((value) => shared.information = value);

          Navigator.pop(context);
        },
      );
    });
  }
}
