// validators.dart

/// Basic YYYY-MM-DD format check (does not validate calendar correctness beyond DateTime parsing).
bool isIsoDate(String value) {
  final regex = RegExp(r'^\d{4}-\d{2}-\d{2}$');
  if (!regex.hasMatch(value)) return false;
  try {
    DateTime.parse(value);
    return true;
  } catch (_) {
    return false;
  }
}

/// Returns true if both dates are valid ISO dates and start <= end.
bool isValidDateRange(String start, String end) {
  if (!isIsoDate(start) || !isIsoDate(end)) return false;
  final s = DateTime.parse(start);
  final e = DateTime.parse(end);
  return !s.isAfter(e);
}
