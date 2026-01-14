// save_fitbit_data_page.dart
import 'package:flutter/material.dart';
import 'api_service.dart'; // Import API service
import '../utils/validators.dart';

class SaveFitbitDataPage extends StatefulWidget {
  @override
  _SaveFitbitDataPageState createState() => _SaveFitbitDataPageState();
}

class _SaveFitbitDataPageState extends State<SaveFitbitDataPage> {
  final TextEditingController _dateController = TextEditingController();

  Future<void> _saveFitbitData() async {
    final date = _dateController.text.trim();

    if (!isIsoDate(date)) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Enter a date in YYYY-MM-DD format.')),
      );
      return;
    }

    try {
      await saveHeartRate(date);
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Saved Fitbit data successfully.')),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
            content: Text('Unable to save data. Please try again.')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Save Fitbit Data'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: <Widget>[
            TextField(
              controller: _dateController,
              decoration: const InputDecoration(labelText: 'Date (YYYY-MM-DD)'),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _saveFitbitData,
              child: const Text('Save Data'),
            ),
          ],
        ),
      ),
    );
  }
}
