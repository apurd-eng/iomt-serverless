// stress_checkin_page.dart
import 'package:flutter/material.dart';

class StressCheckInPage extends StatefulWidget {
  @override
  _StressCheckInPageState createState() => _StressCheckInPageState();
}

class _StressCheckInPageState extends State<StressCheckInPage> {
  final TextEditingController _stressController = TextEditingController();

  void _submitStress() {
    String stressScore = _stressController.text;
    // Here you would call your backend API to save the stress score.
    // Placeholder for API endpoint: YOUR_API_ENDPOINT_HERE
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Stress score submitted: $stressScore')),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Daily Stress Check-In'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: <Widget>[
            const Text('Please rate your stress level today:'),
            TextField(
              controller: _stressController,
              keyboardType: TextInputType.number,
              decoration:
                  const InputDecoration(labelText: 'Stress Score (1-10)'),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _submitStress,
              child: const Text('Submit Stress Score'),
            )
          ],
        ),
      ),
    );
  }
}
