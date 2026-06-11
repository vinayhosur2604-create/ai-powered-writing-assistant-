import os
java_home = os.path.normpath('C:/Program Files/Eclipse Adoptium/jdk-17.0.19.10-hotspot')
if os.path.exists(java_home):
    os.environ['JAVA_HOME'] = java_home
    os.environ['PATH'] = os.path.join(java_home, 'bin') + os.pathsep + os.environ.get('PATH', '')

import language_tool_python

text = 'This are wrong sentence.'
print('text:', text)

tool = language_tool_python.LanguageTool('en-US')
matches = tool.check(text)
print('matches len', len(matches))
for m in matches:
    print('ruleId:', m.ruleId)
    print('message:', m.message)
    print('replacements:', m.replacements)
    print('offset,errorLength:', m.offset, m.errorLength)
    print('context:', m.context)
    print('sentence:', m.sentence)
    print('---')
print('correct:', tool.correct(text))
