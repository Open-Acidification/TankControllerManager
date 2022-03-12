import 'package:flutter/material.dart';
import 'package:tank_manager/view/home_page.dart';
import 'package:provider/provider.dart';
import 'package:tank_manager/model/app_data.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (_) => AppData(),
      child: MaterialApp(
        debugShowCheckedModeBanner: false,
        title: 'Tank Manager',
        theme: ThemeData(
          primarySwatch: Colors.blue,
          scaffoldBackgroundColor: Colors.grey.shade500,
        ),
        home: const MyHomePage(title: 'Tank Manager'),
      ),
    );
  }
}
