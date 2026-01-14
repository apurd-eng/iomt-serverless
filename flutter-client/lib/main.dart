// main.dart
import 'package:flutter/material.dart';
import 'screens/login_page.dart';
import 'screens/main_page.dart';
import 'screens/stress_checkin_page.dart';
import 'screens/fitbit_data_fetch_page.dart';
import 'screens/save_fitbit_data_page.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Daily Stress Monitor',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      initialRoute: '/login',
      routes: {
        '/login': (context) => LoginPage(),
        '/main': (context) => MainPage(),
        '/stressCheckIn': (context) => StressCheckInPage(),
        '/fetchFitbit': (context) => FitbitDataFetchPage(),
        '/saveFitbit': (context) => SaveFitbitDataPage(),
      },
    );
  }
}
