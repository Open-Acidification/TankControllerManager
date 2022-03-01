// This is a basic Flutter widget test.
//
// To perform an interaction with a widget in your test, use the WidgetTester
// utility that Flutter provides. For example, you can send tap and scroll
// gestures. You can also use WidgetTester to find child widgets in the widget
// tree, read text, and verify that the values of widget properties are correct.

import 'package:flutter_test/flutter_test.dart';

import 'package:tank_manager/main.dart';
import 'package:tank_manager/model/tc_interface.dart';

void main() {
  setUp(() => TcInterface.useMock());
  testWidgets('Buttons work as expected', (WidgetTester tester) async {
    var buttons = [
      '1',
      '2',
      '3',
      'A',
      '4',
      '5',
      '6',
      'B',
      '7',
      '8',
      '9',
      'C',
      '*',
      '0',
      '#',
      'D'
    ];
    // Build our app and trigger a frame.
    await tester.pumpWidget(const MyApp());

    // Force button visiblity for tester
    // Verify a buttons exists
    // Verify no button result is already displayed
    // Tap a button and check display
    for (var b in buttons) {
      await tester.ensureVisible(find.text(b));

      expect(find.text(b), findsOneWidget);
      expect(find.text('pH=7.352   7.218\nT=10.99 C 11.00' + b), findsNothing);

      await tester.tap(find.text(b));
      await tester.pump();
      expect(
          find.text('pH=7.352   7.218\nT=10.99 C 11.00' + b), findsOneWidget);
    }
  });
}
