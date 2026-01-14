// main_page.dart
import 'package:flutter/material.dart';

class MainPage extends StatelessWidget {
  void _logout(BuildContext context) {
    Navigator.pushReplacementNamed(context, '/login');
  }

  void _navigateTo(BuildContext context, String route) {
    Navigator.pushNamed(context, route);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Daily Stress Monitor'),
        actions: <Widget>[
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () => _logout(context),
          )
        ],
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            // MainAxisSize.min keeps the column as small as possible.
            mainAxisSize: MainAxisSize.min,
            // Center elements vertically.
            mainAxisAlignment: MainAxisAlignment.center,
            // Make buttons expand horizontally.
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: <Widget>[
              ElevatedButton(
                onPressed: () => _navigateTo(context, '/stressCheckIn'),
                child: const Text('Daily Stress Check-In'),
              ),
              const SizedBox(height: 10),
              ElevatedButton(
                onPressed: () => _navigateTo(context, '/fetchFitbit'),
                child: const Text('Fetch Fitbit Data'),
              ),
              const SizedBox(height: 10),
              ElevatedButton(
                onPressed: () => _navigateTo(context, '/saveFitbit'),
                child: const Text('Save Fitbit Data'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
