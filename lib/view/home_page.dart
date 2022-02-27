import 'package:flutter/material.dart';
import 'package:tank_manager/model/nav_bar.dart';
import 'package:tank_manager/model/tc_interface.dart';
import 'package:tank_manager/model/display.dart';
import 'package:provider/provider.dart';
import 'package:tank_manager/model/shared.dart';
import 'package:tank_manager/model/keypad.dart';
import 'package:tank_manager/model/app_drawer.dart';
import 'package:tank_manager/view/information_page.dart';
import 'graphs_page.dart';

class MyHomePage extends StatefulWidget {
  const MyHomePage({Key? key, required this.title}) : super(key: key);

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  var tcInterface = TcMockInterface();

  Widget appBody(BuildContext context) {
    return Center(
      child: Column(
        children: <Widget>[
          Display(context: context),
          Flexible(
            child: Keypad(context: context),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final List<Widget> _children = [
      appBody(context),
      Information(context: context),
      Graphs(context: context),
    ];
    return Consumer<SHARED>(
      builder: (context, ui, child) {
        return Scaffold(
          appBar: AppBar(
            title: Text(
              widget.title + ': ' + ui.currentTank.name,
            ),
          ),
          drawer: AppDrawer(context: context),
          body: _children[ui.currentIndex],
          bottomNavigationBar: NavBar(context: context),
        );
      },
    );
  }
}
