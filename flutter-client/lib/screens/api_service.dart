// api_service.dart
import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config.dart';

// Keep timeouts short for mobile UX; serverless endpoints should respond quickly.
const Duration _requestTimeout = Duration(seconds: 10);

Uri _buildUri(String path) {
  final base = AppConfig.apiBaseUrl.trim();
  if (base.isEmpty) {
    throw Exception('API_BASE_URL not configured');
  }
  final normalizedBase = base.endsWith('/') ? base.substring(0, base.length - 1) : base;
  final normalizedPath = path.startsWith('/') ? path : '/$path';
  return Uri.parse('$normalizedBase$normalizedPath');
}

Future<String> getHeartRate(String startdate, String enddate) async {
  final url = _buildUri('/getData/HeartRateData');

  final response = await http
      .post(
        url,
        headers: <String, String>{
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: jsonEncode(<String, String>{
          'startdate': startdate,
          'enddate': enddate,
        }),
      )
      .timeout(_requestTimeout);

  if (response.statusCode == 200) {
    final mapbody = jsonDecode(response.body) as Map<String, dynamic>;
    final body = mapbody['body'];
    return body is String ? body : jsonEncode(body);
  }

  // Avoid returning raw server errors to the UI.
  throw Exception('Request failed');
}

Future<String> saveHeartRate(String collect_date) async {
  final url = _buildUri('/getData/saveHeartRate');

  final response = await http
      .post(
        url,
        headers: <String, String>{
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: jsonEncode(<String, String>{
          'collect_date': collect_date,
        }),
      )
      .timeout(_requestTimeout);

  if (response.statusCode == 200) {
    final mapbody = jsonDecode(response.body) as Map<String, dynamic>;
    final body = mapbody['body'];
    return body is String ? body : jsonEncode(body);
  }

  throw Exception('Request failed');
}
