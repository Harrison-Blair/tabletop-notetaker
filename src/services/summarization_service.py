"""
Summarization service for creating notes from transcripts
"""

import json
import re
from typing import Dict, List, Any, Optional
from datetime import datetime


class SummarizationService:
    """Handles transcript summarization and note generation"""

    def __init__(self):
        # Simple keyword-based summarization (can be enhanced with LLM)
        self.common_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
            'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does',
            'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'shall'
        }

    def summarize(self, transcript: Dict[str, Any], format_type: str = "txt") -> str:
        """Summarize transcript into formatted notes"""
        segments = transcript.get('segments', [])

        if not segments:
            return "No transcript content to summarize."

        # Extract key information
        summary_data = self._extract_summary_data(segments)

        # Format based on requested type
        if format_type == "md":
            return self._format_markdown_summary(summary_data, transcript)
        elif format_type == "json":
            return self._format_json_summary(summary_data, transcript)
        else:
            return self._format_text_summary(summary_data, transcript)

    def _extract_summary_data(self, segments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract key information from transcript segments"""
        all_text = []
        speakers = set()
        key_points = []
        action_items = []

        for segment in segments:
            text = segment.get('text', '').strip()
            speaker = segment.get('speaker', 'Unknown')

            if text:
                all_text.append(text)
                speakers.add(speaker)

                # Extract potential action items
                if any(word in text.lower() for word in ['todo', 'need to', 'should', 'will', 'action']):
                    action_items.append(f"{speaker}: {text}")

                # Extract key points (sentences with important indicators)
                sentences = re.split(r'[.!?]+', text)
                for sentence in sentences:
                    sentence = sentence.strip()
                    if len(sentence) > 20:  # Only consider substantial sentences
                        key_points.append(sentence)

        # Extract keywords
        full_text = ' '.join(all_text)
        keywords = self._extract_keywords(full_text)

        return {
            'speakers': list(speakers),
            'total_segments': len(segments),
            'key_points': key_points[:10],  # Limit to top 10
            'action_items': action_items[:5],  # Limit to 5
            'keywords': keywords[:15],  # Limit to 15
            'summary_text': self._generate_summary_text(all_text)
        }

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text"""
        words = re.findall(r'\b\w+\b', text.lower())
        word_freq = {}

        for word in words:
            if len(word) > 3 and word not in self.common_words:
                word_freq[word] = word_freq.get(word, 0) + 1

        # Sort by frequency
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words if freq > 1]

    def _generate_summary_text(self, text_segments: List[str]) -> str:
        """Generate a concise summary of the discussion"""
        full_text = ' '.join(text_segments)

        # Simple extractive summarization
        sentences = re.split(r'[.!?]+', full_text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]

        # Select sentences that seem important
        important_sentences = []
        for sentence in sentences[:5]:  # Take first 5 substantial sentences
            if len(important_sentences) < 3:  # Limit to 3
                important_sentences.append(sentence)

        return ' '.join(important_sentences)

    def _format_text_summary(self, data: Dict[str, Any], transcript: Dict[str, Any]) -> str:
        """Format summary as plain text"""
        lines = []
        lines.append("MEETING SUMMARY")
        lines.append("=" * 50)
        lines.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Duration: {transcript.get('duration', 'Unknown')} seconds")
        lines.append("")

        lines.append("PARTICIPANTS:")
        for speaker in data['speakers']:
            lines.append(f"  - {speaker}")
        lines.append("")

        if data['summary_text']:
            lines.append("SUMMARY:")
            lines.append(data['summary_text'])
            lines.append("")

        if data['key_points']:
            lines.append("KEY POINTS:")
            for i, point in enumerate(data['key_points'], 1):
                lines.append(f"  {i}. {point}")
            lines.append("")

        if data['action_items']:
            lines.append("ACTION ITEMS:")
            for i, item in enumerate(data['action_items'], 1):
                lines.append(f"  {i}. {item}")
            lines.append("")

        if data['keywords']:
            lines.append("TOPICS/KEYWORDS:")
            lines.append(", ".join(data['keywords']))

        return "\n".join(lines)

    def _format_markdown_summary(self, data: Dict[str, Any], transcript: Dict[str, Any]) -> str:
        """Format summary as Markdown"""
        lines = []
        lines.append("# Meeting Summary")
        lines.append("")
        lines.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"**Duration:** {transcript.get('duration', 'Unknown')} seconds")
        lines.append("")

        lines.append("## Participants")
        for speaker in data['speakers']:
            lines.append(f"- {speaker}")
        lines.append("")

        if data['summary_text']:
            lines.append("## Summary")
            lines.append(data['summary_text'])
            lines.append("")

        if data['key_points']:
            lines.append("## Key Points")
            for point in data['key_points']:
                lines.append(f"- {point}")
            lines.append("")

        if data['action_items']:
            lines.append("## Action Items")
            for item in data['action_items']:
                lines.append(f"- {item}")
            lines.append("")

        if data['keywords']:
            lines.append("## Topics/Keywords")
            lines.append(", ".join(data['keywords']))

        return "\n".join(lines)

    def _format_json_summary(self, data: Dict[str, Any], transcript: Dict[str, Any]) -> str:
        """Format summary as JSON"""
        summary = {
            'metadata': {
                'date': datetime.now().isoformat(),
                'duration': transcript.get('duration', 0),
                'file_path': transcript.get('file_path', '')
            },
            'participants': data['speakers'],
            'summary': data['summary_text'],
            'key_points': data['key_points'],
            'action_items': data['action_items'],
            'keywords': data['keywords']
        }
        return json.dumps(summary, indent=2, ensure_ascii=False)
