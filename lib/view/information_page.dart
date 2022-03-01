import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:tank_manager/model/app_data.dart';

class Information extends StatelessWidget {
  const Information({
    Key? key,
    required this.context,
  }) : super(key: key);

  final BuildContext context;

  @override
  Widget build(BuildContext context) {
    return Consumer<AppData>(
      builder: (context, ui, child) {
        return RichText(
          text: TextSpan(
            text: ui.information,
          ),
        );
      },
    );
  }
}
