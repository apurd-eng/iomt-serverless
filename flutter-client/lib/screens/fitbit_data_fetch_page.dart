// fitbit_data_fetch_page.dart
import 'package:flutter/material.dart';
import 'api_service.dart'; // Import API service
import '../utils/validators.dart';

class FitbitDataFetchPage extends StatefulWidget {
  @override
  _FitbitDataFetchPageState createState() => _FitbitDataFetchPageState();
}

class _FitbitDataFetchPageState extends State<FitbitDataFetchPage> {
  final TextEditingController _startDateController = TextEditingController();
  final TextEditingController _endDateController = TextEditingController();

  String _fetchedData = '';

  Future<void> _fetchFitbitData() async {
    final startDate = _startDateController.text.trim();
    final endDate = _endDateController.text.trim();

    if (!isValidDateRange(startDate, endDate)) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text(
            'Enter valid dates in YYYY-MM-DD format (start must be on or before end).',
          ),
        ),
      );
      return;
    }

    try {
      final result = await getHeartRate(startDate, endDate);
      setState(() {
        _fetchedData = result;
      });
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Fetched Fitbit data successfully.')),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
            content: Text('Unable to fetch data. Please try again.')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Fetch Fitbit Data'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: <Widget>[
            TextField(
              controller: _startDateController,
              decoration:
                  const InputDecoration(labelText: 'Start Date (YYYY-MM-DD)'),
            ),
            TextField(
              controller: _endDateController,
              decoration:
                  const InputDecoration(labelText: 'End Date (YYYY-MM-DD)'),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _fetchFitbitData,
              child: const Text('Fetch Data'),
            ),
            const SizedBox(height: 20),
            // Wrap the fetched data text in an Expanded SingleChildScrollView
            Expanded(
              child: SingleChildScrollView(
                child: Text(
                  _fetchedData,
                  style: const TextStyle(fontSize: 16),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
