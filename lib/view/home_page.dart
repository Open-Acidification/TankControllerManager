import 'package:flutter/material.dart';
import 'package:tank_manager/model/tc_interface.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'dart:convert';

class MyHomePage extends StatefulWidget {
  const MyHomePage({Key? key, required this.title}) : super(key: key);

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class Tank<T1, T2> {
  final T1 name;
  final T2 ip;

  Tank(this.name, this.ip);

  Map toJson() => {
        'name': name,
        'ip': ip,
      };

  Tank.fromJson(Map json)
      : name = json['name'],
        ip = json['ip'];

  @override
  bool operator ==(Object other) => hashCode == other.hashCode;

  @override
  int get hashCode => name.hashCode;
}

class _MyHomePageState extends State<MyHomePage> {
  var tcInterface = TcMockInterface();
  var display = '';
  var informationJson = '';
  final ipController = TextEditingController();
  final nameController = TextEditingController();
  dynamic currentTank = Tank('', '');
  dynamic tanksList = [];
  int _currentIndex = 0;
  String json = '';

  Widget button(var label, var color) {
    return Container(
      padding: const EdgeInsets.all(8),
      decoration: BoxDecoration(
          color: color,
          border: Border.all(width: 5, color: Colors.white),
          borderRadius: const BorderRadius.all(Radius.circular(20))),
      child: TextButton(
        style: TextButton.styleFrom(
          textStyle: const TextStyle(fontSize: 40),
          primary: Colors.white,
        ),
        onPressed: () {
          if (currentTank != Tank('', '')) {
            tcInterface.post(currentTank.ip, 'key?value=$label').then(
                  (value) => setState(
                    () {
                      display = value;
                    },
                  ),
                );
          }
        },
        child: Text(label),
      ),
    );
  }

  Widget tile(var selected) {
    return ListTile(
      title: Text(
        selected.name,
        style: const TextStyle(color: Colors.white),
      ),
      onTap: () {
        setState(() {
          currentTank = selected;
        });

        Navigator.pop(context);
      },
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

  List<Widget> tiles(BuildContext context) {
    var result = <Widget>[];
    for (var each in tanksList) {
      result.add(tile(each));
    }
    return result;
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

  Widget appDrawer(BuildContext context) {
    return Drawer(
      backgroundColor: Colors.grey.shade600,
      child: ListView(
        padding: EdgeInsets.zero,
        children: [
          drawerHeader(context),
          ...tiles(context),
          field(nameController, 'Name', 'Tank 99'),
          field(ipController, 'IP', '000.000.000.000'),
          Align(
            alignment: Alignment.topRight,
            child: FloatingActionButton(
              onPressed: () {
                setState(() {
                  var newTank = Tank(nameController.text, ipController.text);
                  tanksList.add(newTank);
                  saveObj1();

                  nameController.text = "";
                  ipController.text = "";
                });
              },
              tooltip: 'Add Tank',
              child: const Icon(Icons.add),
            ),
          )
        ],
      ),
    );
  }

  Widget keypad(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        borderRadius: const BorderRadius.all(Radius.circular(20)),
        color: Colors.grey.shade800,
        border: Border.all(width: 3.0, color: Colors.white),
      ),
      height: 415,
      width: 415,
      child: GridView.count(
        primary: false,
        padding: const EdgeInsets.all(20),
        crossAxisSpacing: 10,
        mainAxisSpacing: 10,
        crossAxisCount: 4,
        children: buttons(context),
      ),
    );
  }

  List<Widget> buttons(BuildContext context) {
    return <Widget>[
      button('1', Colors.blue),
      button('2', Colors.blue),
      button('3', Colors.blue),
      button('A', Colors.red),
      button('4', Colors.blue),
      button('5', Colors.blue),
      button('6', Colors.blue),
      button('B', Colors.red),
      button('7', Colors.blue),
      button('8', Colors.blue),
      button('9', Colors.blue),
      button('C', Colors.red),
      button('*', Colors.red),
      button('0', Colors.blue),
      button('#', Colors.red),
      button('D', Colors.red),
    ];
  }

  Widget lcdDisplay(BuildContext context) {
    return InkWell(
      splashColor: Colors.grey.shade300,
      onTap: () {
        updateDisplay();
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
        child: Text(
          display,
          textAlign: TextAlign.center,
          style: GoogleFonts.vt323(
            fontSize: 35,
            color: Colors.white,
            letterSpacing: 3,
          ),
        ),
      ),
    );
  }

  Widget appBody(BuildContext context) {
    return Center(
      child: Column(
        children: <Widget>[
          lcdDisplay(context),
          Flexible(
            child: keypad(context),
          ),
        ],
      ),
    );
  }

  void updateDisplay() async {
    if (display == '' && currentTank != Tank('', '')) {
      tcInterface.get(currentTank.ip, 'display').then((value) {
        setState(() {
          display = value;
        });
      });
    }
  }

  void updateInformation() async {
    if (currentTank != Tank('', '')) {
      tcInterface.get(currentTank.ip, 'current').then((value) {
        setState(() {
          informationJson = value;
        });
      });
    }
  }

  void onTabTapped(int index) {
    setState(() {
      _currentIndex = index;
    });
  }

  Widget navBar(BuildContext context) {
    return BottomNavigationBar(
      currentIndex: _currentIndex,
      onTap: onTabTapped,
      backgroundColor: Colors.grey.shade800,
      selectedItemColor: Colors.blue,
      unselectedItemColor: Colors.white,
      items: const <BottomNavigationBarItem>[
        BottomNavigationBarItem(
          icon: Icon(Icons.apps),
          label: 'Keypad',
        ),
        BottomNavigationBarItem(
          icon: Icon(Icons.event_note_outlined),
          label: 'Information',
        ),
        BottomNavigationBarItem(
          icon: Icon(Icons.bar_chart_rounded),
          label: 'Graphs',
        ),
      ],
    );
  }

  Widget information(BuildContext context) {
    return Container(
      color: Colors.green,
      child: Text(informationJson),
    );
  }

  Widget graphs(BuildContext context) {
    return Container(color: Colors.purple);
  }

  saveObj1() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    prefs.setString('obj1', jsonEncode(tanksList));
  }

  getObj1() async {
    if (tanksList.isNotEmpty) return;
    SharedPreferences prefs = await SharedPreferences.getInstance();
    if (prefs.containsKey('obj1')) {
      String obj1 = prefs.getString('obj1')!;
      setState(() {
        decodeObj1(obj1);
      });
    }
  }

  decodeObj1(obj1) {
    tanksList =
        List<Tank>.from(jsonDecode(obj1).map((obj1) => Tank.fromJson(obj1)));
  }

  @override
  Widget build(BuildContext context) {
    final List<Widget> _children = [
      appBody(context),
      information(context),
      graphs(context),
    ];
    getObj1();
    updateDisplay();
    updateInformation();
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title + ': ' + currentTank.name),
      ),
      drawer: appDrawer(context),
      body: _children[_currentIndex],
      bottomNavigationBar: navBar(context),
    );
  }
}
