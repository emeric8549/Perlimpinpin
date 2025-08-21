import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Dev Coach',
      home: RepoSuggestionScreen(),
    );
  }
}

class TaskSuggestion {
  final String title;
  final String file;
  final String description;
  final int estimatedTime;

  TaskSuggestion({
    required this.title,
    required this.file,
    required this.description,
    required this.estimatedTime,
  });

  factory TaskSuggestion.fromJson(Map<String, dynamic> json) {
    return TaskSuggestion(
      title: json['title'],
      file: json['file'],
      description: json['description'],
      estimatedTime: json['estimated_time'],
    );
  }
}

class RepoSuggestionScreen extends StatefulWidget {
  @override
  _RepoSuggestionScreenState createState() => _RepoSuggestionScreenState();
}

class _RepoSuggestionScreenState extends State<RepoSuggestionScreen> {
  final TextEditingController _repoController = TextEditingController();
  final TextEditingController _timeController = TextEditingController();
  List<TaskSuggestion> _suggestions = [];
  String _error = '';
  bool _isLoading = false;

  Future<void> fetchSuggestion(String repoUrl, int timeLimit) async {
    setState(() {
      _isLoading = true;
      _error = '';
      _suggestions = [];
    });

    final uri = Uri.parse('http://localhost:8000/generate-tasks');
    try {
      final response = await http.post(
        uri,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'github_url': repoUrl,
          'time_minutes': timeLimit,
        }),
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        final suggestions = data.map((e) => TaskSuggestion.fromJson(e)).toList();

        setState(() {
          _suggestions = suggestions;
        });
      } else {
        setState(() {
          _error = 'Error: ${response.statusCode}';
        });
      }
    } catch (e) {
      setState(() {
        _error = 'Error: $e';
      });
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  void _onSubmit() {
    final repoUrl = _repoController.text.trim();
    final timeStr = _timeController.text.trim();
    if (repoUrl.isEmpty || timeStr.isEmpty) return;

    final timeLimit = int.tryParse(timeStr);
    if (timeLimit == null || timeLimit <= 0) {
      setState(() => _error = 'Please enter a valid number of minutes.');
      return;
    }

    fetchSuggestion(repoUrl, timeLimit);
  }

  Widget _buildSuggestionCard(TaskSuggestion suggestion) {
    return Card(
      margin: EdgeInsets.symmetric(vertical: 8),
      child: Padding(
        padding: EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(suggestion.title, style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            SizedBox(height: 4),
            Text('File: ${suggestion.file}', style: TextStyle(fontStyle: FontStyle.italic)),
            SizedBox(height: 6),
            Text(suggestion.description),
            SizedBox(height: 6),
            Text('Estimated time: ${suggestion.estimatedTime} min', style: TextStyle(color: Colors.blue)),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Dev Coach')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: _repoController,
              decoration: InputDecoration(
                labelText: 'GitHub Repository URL',
                border: OutlineInputBorder(),
              ),
            ),
            SizedBox(height: 12),
            TextField(
              controller: _timeController,
              decoration: InputDecoration(
                labelText: 'Time Available (minutes)',
                border: OutlineInputBorder(),
              ),
              keyboardType: TextInputType.number,
            ),
            SizedBox(height: 12),
            ElevatedButton(
              onPressed: _onSubmit,
              child: Text('Get Suggestions'),
            ),
            SizedBox(height: 20),
            if (_isLoading)
              CircularProgressIndicator()
            else if (_error.isNotEmpty)
              Text(_error, style: TextStyle(color: Colors.red))
            else if (_suggestions.isNotEmpty)
              Expanded(
                child: ListView.builder(
                  itemCount: _suggestions.length,
                  itemBuilder: (context, index) =>
                      _buildSuggestionCard(_suggestions[index]),
                ),
              )
            else
              Text('No suggestions yet.'),
          ],
        ),
      ),
    );
  }
}