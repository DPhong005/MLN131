from pathlib import Path

root = Path(__file__).resolve().parent.parent
p = root / 'js/app.js'
s = p.read_text(encoding='utf-8')
s = '\n'.join(line for line in s.split('\n') if not line.startswith(('function essayCard(', 'function bindEssays(')))
s = s.replace('${essayCard(c)}', '').replace(' bindEssays();', '')
start = s.index('function renderPractice()')
end = s.index('\n', start)
line = s[start:end]
line = line.replace('42 câu trắc nghiệm có giải thích và nguồn, cùng 7 câu tự luận để rèn lập luận.', '42 câu trắc nghiệm có giải thích và nguồn.')
line = line.replace('<button class="filter-button active" data-practice="quiz">Trắc nghiệm</button><button class="filter-button" data-practice="essay">Tự luận</button>', '<span class="tag">Trắc nghiệm</span>')
line = line.replace("let mode='quiz';", '')
line = line.replace("mode==='essay'?`<div class=\"grid\">${list.map(essayCard).join('')}</div>`:", '')
line = line.replace('bindEssays();', '')
listener_start = line.index("$$('[data-practice]')")
listener_end = line.index("$('#chapter-filter').addEventListener", listener_start)
line = line[:listener_start] + line[listener_end:]
s = s[:start] + line + s[end:]
s = s.replace('Luyện tập và tự luận', 'Luyện tập trắc nghiệm')
s = s.replace('Tiến độ và bài tự luận', 'Tiến độ học tập')
s = s.replace('Bài tự luận, điểm và các dấu đã đọc sẽ được đặt lại.', 'Điểm và các dấu đã đọc sẽ được đặt lại.')
p.write_text(s, encoding='utf-8')
p = root / 'tests/browser/site.spec.cjs'
s = p.read_text(encoding='utf-8').replace('reading progress, essays and accent-insensitive search survive reload', 'reading progress and accent-insensitive search survive reload')
s = '\n'.join(line for line in s.split('\n') if "page.locator('#essay-text-2').fill" not in line)
p.write_text(s, encoding='utf-8')
