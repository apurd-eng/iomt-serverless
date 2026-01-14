// config.dart
// Configure at build time with:
// flutter run --dart-define=API_BASE_URL=https://YOUR_API.execute-api.REGION.amazonaws.com
class AppConfig {
  static const String apiBaseUrl =
      String.fromEnvironment('API_BASE_URL', defaultValue: '');
}
