# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib import colors
# from reportlab.lib.units import inch
# from datetime import datetime
# import json
# import re
# import os
# from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.ttfonts import TTFont
# from LLM_Module.Overall_Analyser import VideoResumeEvaluator 
# from config import save_path

# # Register fonts
# pdfmetrics.registerFont(TTFont('Arial', r'ARIAL.TTF'))
# pdfmetrics.registerFont(TTFont('Arial-Bold', r'ArialBD.ttf'))
# styles = getSampleStyleSheet()
# styles['BodyText'].fontName = 'Arial'

# def create_combined_pdf(logo_path, json_path, output_pdf_path):
#     # Read presentation mode info
#     with open("json/presentation.json", "r") as file:
#         data = json.load(file)
#     presentation_mode = data.get("presentation_mode", False)
    
#     # Read main JSON data
#     with open(json_path, 'r') as fp:
#         tabular_data = json.load(fp)
    
#     # Read quality score data for middle column values
#     with open(r'json/scores.json', 'r') as fp:
#         quality_data = json.load(fp)
#         midval = list(quality_data.values())
        
#     # Set questions based on presentation mode
#     if presentation_mode == 'on':
#         llm_questions = [
#             "Questions", 
#             "Did the Speaker Speak with Confidence ?", 
#             "Did the speaker vary their tone, speed, volume while delivering the speech/presentation? ",
#             "Did the speech have a structure of Opening, Body and Conclusion? ",
#             "Was the overall “Objective” of the speech delivered clearly?",
#             "Was the content of the presentation/speech brief and to the point, or did it include unnecessary details that may have distracted or confused the audience?",
#             "Was the content of the presentation/speech engaging, and did it capture the audience’s attention?", 
#             "Was the content of the presentation/speech relevant to the objective of the presentation?", 
#             "Was the content of the presentation/speech clear and easy to understand?", 
#             "Did the speaker add relevant examples, anecdotes and data to back their content?",
#             "Did the speaker demonstrate credibility? Will you trust the speaker?", 
#             "Did the speaker clearly explain how the speech or topic would benefit you and what you could gain from it?", 
#             "Was the speaker able to evoke an emotional connection with the audience?", 
#             "Overall, were you convinced/ persuaded with the speaker’s view on the topic?"
#         ]
#     else: 
#         llm_questions = [
#             "Questions", 
#             "Did the Speaker Speak with Confidence ?", 
#             "Was the content interesting and as per the guidelines provided?",
#             "Who are you and what are your skills, expertise, and personality traits?",
#             "Why are you the best person to fit this role?",
#             "How are you different from others?",
#             "What value do you bring to the role?",
#             "Did the speech have a structure of Opening, Body, and Conclusion?",
#             "Did the speaker vary their tone, speed, and volume while delivering the speech/presentation?", 
#             "How was the quality of research for the topic? Did the speech demonstrate good depth? Did they cite sources?",
#             "How convinced were you with the overall speech on the topic? Was it persuasive? Will you consider them for the job/opportunity?"
#         ]

#     def clean_answer(answer):
#         return re.sub(r'^\d+\.\s*', '', answer).strip()

#     llm_answers = []
#     if 'LLM' in tabular_data:
#         llm_answers = re.split(r'\n(?=\d+\.)', tabular_data['LLM'])

#     # Create document using the passed output path
#     doc = SimpleDocTemplate(output_pdf_path, 
#                             pagesize=letter,
#                             topMargin=1.5*inch,
#                             bottomMargin=0.8*inch)
#     flowables = []
#     styles = getSampleStyleSheet()

#     def add_header_footer(canvas, doc):
#         canvas.saveState()
#         logo = Image(logo_path, width=2*inch, height=1*inch)
#         logo.drawOn(canvas, (letter[0]-2*inch)/2, letter[1]-1.2*inch)
#         website_text = "https://some.education.in"
#         canvas.setFont("Arial", 9)
#         canvas.linkURL("https://some.education.in",
#                        (0.5*inch, 0.3*inch, 2.5*inch, 0.5*inch),
#                        relative=1)
#         canvas.drawString(0.5*inch, 0.3*inch, website_text)
#         page_num = canvas.getPageNumber()
#         canvas.drawRightString(letter[0]-0.5*inch, 0.3*inch, f"Page {page_num}")
#         canvas.restoreState()

#     section_style = ParagraphStyle(
#         'SectionStyle',
#         parent=styles['BodyText'],
#         fontName='Arial-Bold',
#         fontSize=10,
#         spaceAfter=12,
#         leading=16
#     )
#     bullet_style = ParagraphStyle(
#         'BulletStyle',
#         parent=styles['BodyText'],
#         fontSize=10,
#         leading=14,
#         spaceAfter=6,
#         leftIndent=10
#     )

#     name = tabular_data.get('User Name', 'Unknown Candidate')
#     now = datetime.now()
#     formatted_date = now.strftime("%d %B %Y")
#     title = Paragraph(
#         f"<para alignment='center'><b>{name}</b><br/></para>"
#         f"<para alignment='center'>{formatted_date}</para>", 
#         styles['Title']
#     )
#     flowables.append(title)
#     flowables.append(Spacer(1, 24))

#     def add_quality_section(title, items):
#         flowables.append(Paragraph(title, section_style))
#         bullet_list = []
#         for item in items:
#             bullet_list.append(Paragraph(f"• {item}", bullet_style))
#         flowables.extend(bullet_list)
#         flowables.append(Spacer(1, 18))
    
#     try:
#         with open(r'json/quality_analysis.json', 'r') as fp:
#             quality_data = json.load(fp)
#         add_quality_section("Qualitative Analysis - Positive", quality_data["Qualitative Analysis"])
#         add_quality_section("Qualitative Analysis - Areas of Improvement", quality_data["Quantitative Analysis"])
#     except:
#         pass

#     flowables.append(Spacer(1, 18))
#     flowables.append(PageBreak())

#     section_style = ParagraphStyle('SectionStyle', parent=styles['BodyText'], fontName='Helvetica-Bold', fontSize=10, spaceAfter=12, leading=16)
#     flowables.append(Paragraph("<b>Detailed Evaluation Metrics</b>", section_style))
#     flowables.append(Spacer(1, 24))

#     normal_style = ParagraphStyle('NormalStyle', parent=styles['BodyText'], fontSize=10, leading=12, spaceAfter=6)
#     bold_style = ParagraphStyle('BoldStyle', parent=normal_style, fontName='Helvetica-Bold')

#     # Create table data with a new middle column
#     table_data = [
#         [
#             Paragraph("<b>No.</b>", bold_style),
#             Paragraph("<b>Items to look out for</b>", bold_style),
#             Paragraph("<b>Middle Column</b>", bold_style),
#             Paragraph("<b>5 point scale / Answer</b>", bold_style)
#         ]
#     ]

#     for i, question in enumerate(llm_questions[1:], 1):
#         print("I VALUE -->", i)
#         print("MID VAL -->", midval)
#         if i == 1:
#             sub_items = [
#                 ("Posture", "posture"),
#                 ("Smile", "Smile Score"),
#                 ("Eye Contact", "Eye Contact"),
#                 ("Energetic Start", "Energetic Start")
#             ]
#             items_text = "Did the speaker speak with confidence?<br/>" + "<br/>".join([f"• {item[0]}" for item in sub_items])
#             scores = []
#             for item in sub_items:
#                 key = item[1]
#                 metric_value = tabular_data.get(key)
#                 if metric_value == 1:
#                     scores.append("Needs Improvement")
#                 elif metric_value == 2:
#                     scores.append("Poor")
#                 elif metric_value == 3:
#                     scores.append("Satisfactory")
#                 elif metric_value == 4:
#                     scores.append("Good")
#                 elif metric_value == 5:
#                     scores.append("Excellent")
#                 else:
#                     scores.append("Poor")
#             scores_text = "<br/>" + "<br/>".join([f"<b>{score}</b>" for score in scores])
#             print(" I ---- >", i - 1, midval[i-1])
#             table_data.append([
#                 Paragraph(f"{i}.", normal_style),
#                 Paragraph(items_text, normal_style),
#                 Paragraph(midval[i - 1], normal_style),
#                 Paragraph(scores_text, normal_style)
#             ])
#         else:
#             answer_index = i if i < len(llm_answers) else None
#             if answer_index is not None:
#                 answer = clean_answer(llm_answers[answer_index])
#             else:
#                 answer = "N/A"
#             print(" I ---- >", i - 1, midval[i-1])
#             table_data.append([
#                 Paragraph(f"{i}.", normal_style),
#                 Paragraph(question, normal_style),
#                 Paragraph(midval[i - 1], normal_style),
#                 Paragraph(answer, normal_style)
#             ])

#     # Build the table with defined column widths
#     table = Table(table_data, colWidths=[40, 250, 80, 200])
#     table.setStyle(TableStyle([
#         ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
#         ('VALIGN', (0, 0), (-1, -1), 'TOP'),
#         ('FONTSIZE', (0, 0), (-1, -1), 10),
#         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#         ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
#         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#         ('TOPPADDING', (0, 1), (-1, -1), 6),
#         ('LEFTPADDING', (0, 0), (-1, -1), 4),
#         ('RIGHTPADDING', (0, 0), (-1, -1), 4),
#     ]))
#     flowables.append(table)

#     doc.build(flowables,
#               onFirstPage=add_header_footer,
#               onLaterPages=add_header_footer)

#     print("PDF generated successfully with dynamic table!")


# if __name__ == "__main__":
#     create_combined_pdf(r"logos\logo.png", r"json\output.json", r"reports\combined_report.pdf")

#--------------














# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib import colors
# from reportlab.lib.units import inch
# from datetime import datetime
# import json
# import re
# import os
# from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.ttfonts import TTFont
# from LLM_Module.Overall_Analyser import VideoResumeEvaluator 
# from config import save_path

# # Register fonts
# pdfmetrics.registerFont(TTFont('Arial', r'ARIAL.TTF'))
# pdfmetrics.registerFont(TTFont('Arial-Bold', r'ArialBD.ttf'))
# styles = getSampleStyleSheet()
# styles['BodyText'].fontName = 'Arial'

# def create_combined_pdf(logo_path, json_path, output_pdf_path):
#     # Read presentation mode info
#     with open("json/presentation.json", "r") as file:
#         data = json.load(file)
#     presentation_mode = data.get("presentation_mode", False)
    
#     # Read main JSON data
#     with open(json_path, 'r') as fp:
#         tabular_data = json.load(fp)
    
#     # Read quality score data for middle column values
#     with open(r'json/scores.json', 'r') as fp:
#         quality_data = json.load(fp)
#         # midval is a list of textual ratings (e.g., "Excellent", "Good", etc.)
#         midval = list(quality_data.values())
        
#     # Set questions based on presentation mode
#     if presentation_mode == 'on':
#         llm_questions = [
#             "Questions", 
#             "Did the Speaker Speak with Confidence ?", 
#             "Did the speaker vary their tone, speed, volume while delivering the speech/presentation? ",
#             "Did the speech have a structure of Opening, Body and Conclusion? ",
#             "Was the overall “Objective” of the speech delivered clearly?",
#             "Was the content of the presentation/speech brief and to the point, or did it include unnecessary details that may have distracted or confused the audience?",
#             "Was the content of the presentation/speech engaging, and did it capture the audience’s attention?", 
#             "Was the content of the presentation/speech relevant to the objective of the presentation?", 
#             "Was the content of the presentation/speech clear and easy to understand?", 
#             "Did the speaker add relevant examples, anecdotes and data to back their content?",
#             "Did the speaker demonstrate credibility? Will you trust the speaker?", 
#             "Did the speaker clearly explain how the speech or topic would benefit you and what you could gain from it?", 
#             "Was the speaker able to evoke an emotional connection with the audience?", 
#             "Overall, were you convinced/ persuaded with the speaker’s view on the topic?"
#         ]
#     else: 
#         llm_questions = [
#             "Questions", 
#             "Did the Speaker Speak with Confidence ?", 
#             "Was the content interesting and as per the guidelines provided?",
#             "Who are you and what are your skills, expertise, and personality traits?",
#             "Why are you the best person to fit this role?",
#             "How are you different from others?",
#             "What value do you bring to the role?",
#             "Did the speech have a structure of Opening, Body, and Conclusion?",
#             "Did the speaker vary their tone, speed, and volume while delivering the speech/presentation?", 
#             "How was the quality of research for the topic? Did the speech demonstrate good depth? Did they cite sources?",
#             "How convinced were you with the overall speech on the topic? Was it persuasive? Will you consider them for the job/opportunity?"
#         ]

#     def clean_answer(answer):
#         return re.sub(r'^\d+\.\s*', '', answer).strip()

#     llm_answers = []
#     if 'LLM' in tabular_data:
#         llm_answers = re.split(r'\n(?=\d+\.)', tabular_data['LLM'])

#     # Score mapping for textual ratings to numeric values
#     score_mapping = {
#         "Excellent": 5,
#         "Good": 4,
#         "Satisfactory": 3,
#         "Needs Improvement": 2,
#         "Poor": 1
#     }
#     # Compute total score from the midval list using the mapping (if rating is not found, ignore it)
#     total_score = 0
#     for rating in midval:
#         total_score += score_mapping.get(rating, 0)

#     # Create document using the passed output path
#     doc = SimpleDocTemplate(output_pdf_path, 
#                             pagesize=letter,
#                             topMargin=1.5*inch,
#                             bottomMargin=0.8*inch)
#     flowables = []
#     styles = getSampleStyleSheet()

#     def add_header_footer(canvas, doc):
#         canvas.saveState()
#         logo = Image(logo_path, width=2*inch, height=1*inch)
#         logo.drawOn(canvas, (letter[0]-2*inch)/2, letter[1]-1.2*inch)
#         website_text = "https://some.education.in"
#         canvas.setFont("Arial", 9)
#         canvas.linkURL("https://some.education.in",
#                        (0.5*inch, 0.3*inch, 2.5*inch, 0.5*inch),
#                        relative=1)
#         canvas.drawString(0.5*inch, 0.3*inch, website_text)
#         page_num = canvas.getPageNumber()
#         canvas.drawRightString(letter[0]-0.5*inch, 0.3*inch, f"Page {page_num}")
#         canvas.restoreState()

#     # Define styles
#     section_style = ParagraphStyle(
#         'SectionStyle',
#         parent=styles['BodyText'],
#         fontName='Arial-Bold',
#         fontSize=10,
#         spaceAfter=12,
#         leading=16
#     )
#     bullet_style = ParagraphStyle(
#         'BulletStyle',
#         parent=styles['BodyText'],
#         fontSize=10,
#         leading=14,
#         spaceAfter=6,
#         leftIndent=10
#     )

#     # Candidate name and date at the top
#     name = tabular_data.get('User Name', 'Unknown Candidate')
#     now = datetime.now()
#     formatted_date = now.strftime("%d %B %Y")
#     title = Paragraph(
#         f"<para alignment='center'><b>{name}</b><br/></para>"
#         f"<para alignment='center'>{formatted_date}</para>", 
#         styles['Title']
#     )
#     flowables.append(title)
#     flowables.append(Spacer(1, 12))

#     # NEW: Insert "Assessment" header and Total Score calculation
#     assessment_header = Paragraph("<b>Assessment</b>", section_style)
#     assessment_total = Paragraph(f"Total Score: {total_score}", styles['BodyText'])
#     flowables.append(assessment_header)
#     flowables.append(Spacer(1, 6))
#     flowables.append(assessment_total)
#     flowables.append(Spacer(1, 18))

#     def add_quality_section(title_text, items):
#         flowables.append(Paragraph(title_text, section_style))
#         bullet_list = []
#         for item in items:
#             bullet_list.append(Paragraph(f"• {item}", bullet_style))
#         flowables.extend(bullet_list)
#         flowables.append(Spacer(1, 18))
    
#     try:
#         with open(r'json/quality_analysis.json', 'r') as fp:
#             quality_data_tmp = json.load(fp)
#         add_quality_section("Qualitative Analysis - Positive", quality_data_tmp["Qualitative Analysis"])
#         add_quality_section("Qualitative Analysis - Areas of Improvement", quality_data_tmp["Quantitative Analysis"])
#     except:
#         pass

#     flowables.append(Spacer(1, 18))
#     flowables.append(PageBreak())

#     # Heading for the Evaluation Metrics table
#     section_style_table = ParagraphStyle('SectionStyle', parent=styles['BodyText'], fontName='Helvetica-Bold', fontSize=10, spaceAfter=12, leading=16)
#     flowables.append(Paragraph("<b>Detailed Evaluation Metrics</b>", section_style_table))
#     flowables.append(Spacer(1, 24))

#     normal_style = ParagraphStyle('NormalStyle', parent=styles['BodyText'], fontSize=10, leading=12, spaceAfter=6)
#     bold_style = ParagraphStyle('BoldStyle', parent=normal_style, fontName='Helvetica-Bold')

#     # Create table with a new middle column
#     table_data = [
#         [
#             Paragraph("<b>No.</b>", bold_style),
#             Paragraph("<b>Individual Parameters</b>", bold_style),
#             Paragraph("<b>5 Point scale: Excellent(5), Good(4), Satisfactory(3), Needs Improvement(2), Poor(1)</b>", bold_style),
#             Paragraph("<b>Feedback</b>", bold_style)
#         ]
#     ]

#     for i, question in enumerate(llm_questions[1:], 1):
#         print("I VALUE -->", i)
#         print("MID VAL -->", midval)
#         # Prepare the middle column text with appended numeric score if available.
#         if i <= len(midval):
#             rating_text = midval[i - 1]
#             if rating_text in score_mapping:
#                 rating_text = f"{rating_text} as {score_mapping[rating_text]}"
#         else:
#             rating_text = "N/A"
            
#         if i == 1:
#             sub_items = [
#                 ("Posture", "posture"),
#                 ("Smile", "Smile Score"),
#                 ("Eye Contact", "Eye Contact"),
#                 ("Energetic Start", "Energetic Start")
#             ]
#             items_text = "Did the speaker speak with confidence?<br/>" + "<br/>".join([f"• {item[0]}" for item in sub_items])
#             scores = []
#             for item in sub_items:
#                 key = item[1]
#                 metric_value = tabular_data.get(key)
#                 if metric_value == 1:
#                     scores.append("Needs Improvement")
#                 elif metric_value == 2:
#                     scores.append("Poor")
#                 elif metric_value == 3:
#                     scores.append("Satisfactory")
#                 elif metric_value == 4:
#                     scores.append("Good")
#                 elif metric_value == 5:
#                     scores.append("Excellent")
#                 else:
#                     scores.append("Poor")
#             scores_text = "<br/>" + "<br/>".join([f"<b>{score}</b>" for score in scores])
#             print(" I ---- >", i - 1, midval[i - 1])
#             table_data.append([
#                 Paragraph(f"{i}.", normal_style),
#                 Paragraph(items_text, normal_style),
#                 Paragraph(rating_text, normal_style),
#                 Paragraph(scores_text, normal_style)
#             ])
#         else:
#             answer_index = i if i < len(llm_answers) else None
#             if answer_index is not None:
#                 answer = clean_answer(llm_answers[answer_index])
#             else:
#                 answer = "N/A"
#             print(" I ---- >", i - 1, midval[i-1])
#             table_data.append([
#                 Paragraph(f"{i}.", normal_style),
#                 Paragraph(question, normal_style),
#                 Paragraph(rating_text, normal_style),
#                 Paragraph(answer, normal_style)
#             ])

#     # Create table with defined column widths
#     table = Table(table_data, colWidths=[40, 250, 80, 200])
#     table.setStyle(TableStyle([
#         ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
#         ('VALIGN', (0, 0), (-1, -1), 'TOP'),
#         ('FONTSIZE', (0, 0), (-1, -1), 10),
#         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#         ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
#         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#         ('TOPPADDING', (0, 1), (-1, -1), 6),
#         ('LEFTPADDING', (0, 0), (-1, -1), 4),
#         ('RIGHTPADDING', (0, 0), (-1, -1), 4),
#     ]))
#     flowables.append(table)

#     doc.build(flowables,
#               onFirstPage=add_header_footer,
#               onLaterPages=add_header_footer)

#     print("PDF generated successfully with dynamic table!")
#     # Optionally remove the temporary file if needed:
#     # os.remove(save_path)

# if __name__ == "__main__":
#     create_combined_pdf(r"logos\logo.png", r"json\output.json", r"reports\combined_report.pdf")



from reportlab.lib.pagesizes import letter 
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime
import json
import re
import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from LLM_Module.Overall_Analyser import VideoResumeEvaluator 
from config import save_path

# Register fonts
pdfmetrics.registerFont(TTFont('Arial', r'fonts/ARIAL.TTF'))
pdfmetrics.registerFont(TTFont('Arial-Bold', r'fonts/ARIALBD.TTF'))
styles = getSampleStyleSheet()
styles['BodyText'].fontName = 'Arial'

def create_combined_pdf(logo_path, json_path, output_pdf_path):
    # Read presentation mode info
    with open("json/presentation.json", "r") as file:
        data = json.load(file)
    presentation_mode = data.get("presentation_mode", False)
    
    # Read main JSON data
    with open(json_path, 'r') as fp:
        tabular_data = json.load(fp)
    
    # Read quality score data for middle column values
    with open(r'json/scores.json', 'r') as fp:
        quality_data = json.load(fp)
        # midval is a list of textual ratings (e.g., "Excellent", "Good", etc.)
        midval = list(quality_data.values())
        
    # Set questions based on presentation mode
    if presentation_mode == 'on':
        llm_questions = [
            "Questions", 
            "Did the Speaker Speak with Confidence ?", 
            "Did the speaker vary their tone, speed, volume while delivering the speech/presentation? ",
            "Did they use any hand or body gesture while speaking? ",
            "Did they have expression on thier face? ", 
            "Did the speech have a structure of Opening, Body and Conclusion? ",
            "Was the overall “Objective” of the speech delivered clearly?",
            "Was the content of the presentation/speech brief and to the point, or did it include unnecessary details that may have distracted or confused the audience?",
            "Was the content of the presentation/speech engaging, and did it capture the audience’s attention?", 
            "Was the content of the presentation/speech relevant to the objective of the presentation?", 
            "Was the content of the presentation/speech clear and easy to understand?", 
            "Did the speaker add relevant examples, anecdotes and data to back their content?",
            "Did the speaker demonstrate credibility? Will you trust the speaker?", 
            "Did the speaker clearly explain how the speech or topic would benefit you and what you could gain from it?", 
            "Was the speaker able to evoke an emotional connection with the audience?", 
            "Overall, were you convinced/ persuaded with the speaker’s view on the topic?"
        ]
    else: 
        llm_questions = [
            "Questions", 
            "Did the Speaker Speak with Confidence ?", 
            "Was the content interesting and as per the guidelines provided?",
            "Did they use any hand or body gesture while speaking? ",
            "Did they have expression on thier face? ", 
            "Who are you and what are your skills, expertise, and personality traits?",
            "Why are you the best person to fit this role?",
            "How are you different from others?",
            "What value do you bring to the role?",
            "Did the speech have a structure of Opening, Body, and Conclusion?",
            "Did the speaker vary their tone, speed, and volume while delivering the speech/presentation?", 
            "How was the quality of research for the topic? Did the speech demonstrate good depth? Did they cite sources?",
            "How convinced were you with the overall speech on the topic? Was it persuasive? Will you consider them for the job/opportunity?"
        ]

    def clean_answer(answer):
        return re.sub(r'^\d+\.\s*', '', answer).strip()

    llm_answers = []
    if 'LLM' in tabular_data:
        llm_answers = re.split(r'\n(?=\d+\.)', tabular_data['LLM'])

    # Score mapping for textual ratings to numeric values
    score_mapping = {
        "Excellent": 5,
        "Good": 4,
        "Satisfactory": 3,
        "Needs Improvement": 2,
        "Poor": 1
    }
    # Compute total score from the midval list using the mapping (if rating is not found, ignore it)
    total_score = 0
    for rating in midval:
        total_score += score_mapping.get(rating, 0)

    # Create document using the passed output path
    doc = SimpleDocTemplate(output_pdf_path, 
                            pagesize=letter,
                            topMargin=1.5*inch,
                            bottomMargin=0.8*inch)
    flowables = []
    styles = getSampleStyleSheet()

    def add_header_footer(canvas, doc):
        canvas.saveState()
        logo = Image(logo_path, width=2*inch, height=1*inch)
        logo.drawOn(canvas, (letter[0]-2*inch)/2, letter[1]-1.2*inch)
        website_text = "https://some.education.in"
        canvas.setFont("Arial", 9)
        canvas.linkURL("https://some.education.in",
                       (0.5*inch, 0.3*inch, 2.5*inch, 0.5*inch),
                       relative=1)
        canvas.drawString(0.5*inch, 0.3*inch, website_text)
        page_num = canvas.getPageNumber()
        canvas.drawRightString(letter[0]-0.5*inch, 0.3*inch, f"Page {page_num}")
        canvas.restoreState()

    # Define styles
    section_style = ParagraphStyle(
        'SectionStyle',
        parent=styles['BodyText'],
        fontName='Arial-Bold',
        fontSize=10,
        spaceAfter=12,
        leading=16
    )
    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=styles['BodyText'],
        fontSize=10,
        leading=14,
        spaceAfter=6,
        leftIndent=10
    )

    # Candidate name and date at the top
    name = tabular_data.get('User Name', 'Unknown Candidate')
    now = datetime.now()
    formatted_date = now.strftime("%d %B %Y")
    title = Paragraph(
        f"<para alignment='center'><b>{name}</b><br/></para>"
        f"<para alignment='center'>{formatted_date}</para>", 
        styles['Title']
    )
    flowables.append(title)
    flowables.append(Spacer(1, 12))

    # Insert "Assessment" header and Total Score calculation
    assessment_header = Paragraph("<b>Assessment</b>", section_style)
    assessment_total = Paragraph(f"Total Score: {total_score}", styles['BodyText'])
    flowables.append(assessment_header)
    flowables.append(Spacer(1, 6))
    flowables.append(assessment_total)
    flowables.append(Spacer(1, 18))

    def add_quality_section(title_text, items):
        flowables.append(Paragraph(title_text, section_style))
        bullet_list = []
        for item in items:
            bullet_list.append(Paragraph(f"• {item}", bullet_style))
        flowables.extend(bullet_list)
        flowables.append(Spacer(1, 18))
    
    try:
        with open(r'json/quality_analysis.json', 'r') as fp:
            quality_data_tmp = json.load(fp)
        add_quality_section("Qualitative Analysis - Positive", quality_data_tmp["Qualitative Analysis"])
        add_quality_section("Qualitative Analysis - Areas of Improvement", quality_data_tmp["Quantitative Analysis"])
    except:
        pass

    flowables.append(Spacer(1, 18))
    # flowables.append(PageBreak())

    # Heading for the Evaluation Metrics table
    section_style_table = ParagraphStyle('SectionStyle', parent=styles['BodyText'], 
                                          fontName='Helvetica-Bold', fontSize=10, spaceAfter=12, leading=16)
    flowables.append(Paragraph("<b>Detailed Evaluation Metrics</b>", section_style_table))
    flowables.append(Spacer(1, 24))

    normal_style = ParagraphStyle('NormalStyle', parent=styles['BodyText'], fontSize=10, leading=12, spaceAfter=6)
    bold_style = ParagraphStyle('BoldStyle', parent=normal_style, fontName='Helvetica-Bold')

    # Create table with the requested structure:
    # Columns: No. | Individual Parameters | 5 Point Scale (header description) | Feedback
    table_data = [
        [
            Paragraph("<b>No.</b>", bold_style),
            Paragraph("<b>Individual Parameters</b>", bold_style),
            Paragraph("<b>5 Point scale: Excellent(5), Good(4), Satisfactory(3), Needs Improvement(2), Poor(1)</b>", bold_style),
            Paragraph("<b>Feedback</b>", bold_style)
        ]
    ]

    for i, question in enumerate(llm_questions[1:], 1):
        # For the middle column, display only the numeric score (if available)
        if i <= len(midval) and midval[i - 1] in score_mapping:
            numeric_score = str(score_mapping[midval[i - 1]])
        else:
            numeric_score = "N/A"
            
        if i == 1:
            sub_items = [
                ("Posture", "posture"),
                ("Smile", "Smile Score"),
                ("Eye Contact", "Eye Contact"),
                ("Energetic Start", "Energetic Start")
            ]
            items_text = "Did the speaker speak with confidence?<br/>" + "<br/>".join([f"• {item[0]}" for item in sub_items])
            scores = []
            numeric_scores = []
            for item in sub_items:
                key = item[1]
                metric_value = tabular_data.get(key)
                numeric_scores.append(f"{metric_value}")
                if metric_value == 1:
                    scores.append("Needs Improvement")
                elif metric_value == 2:
                    scores.append("Poor")
                elif metric_value == 3:
                    scores.append("Satisfactory")
                elif metric_value == 4:
                    scores.append("Good")
                elif metric_value == 5:
                    scores.append("Excellent")
                else:
                    scores.append("Poor")
            scores_text = "<br/>" + "<br/>".join([f"<b>{score}</b>" for score in scores])
            numeric_scores_text = "<br/>" + "<br/>".join([f"<b>{numeric_score}</b>" for numeric_score in numeric_scores])
            table_data.append([
                Paragraph(f"{i}.", normal_style),
                Paragraph(items_text, normal_style),
                Paragraph(numeric_scores_text, normal_style),  
                Paragraph(scores_text, normal_style)
            ])
        elif i == 3:
            # # Sub-items for gesture energy evaluation
            # sub_items = [
            #     ("Gesture Energy", "gesture_energy"),  # Gesture energy data to check
            # ]
            
            # Question text
            items_text = "Did they use any gesture with thier hands or body while speaking?"
            # <br/>" + "<br/>".join([f"• {item[0]}" for item in sub_items])
            # Mapping gesture energy values to feedback
            # Map gesture energy values to both feedback and numeric scores
            gesture_feedback_map = {
                "very high": (
                    "The speaker used excessive hand and body gestures. Reducing the intensity slightly could help avoid distraction and improve clarity.",
                    5
                ),
                "high": (
                    "The speaker used expressive gestures, though slightly overdone. A more measured use of gestures could enhance the overall delivery.",
                    4
                ),
                "medium": (
                    "The speaker maintained a good balance of hand and body gestures, effectively supporting their speech. Great job!",
                    3
                ),
                "low": (
                    "The speaker's gestures were minimal. Adding more expressive movements could make the presentation more engaging.",
                    2
                ),
                "very low": (
                    "The speaker rarely used any gestures. Incorporating some body language could significantly boost engagement.",
                    1
                ),
                "hands not detected": (
                    "Hands not detected. Please move further from the camera to allow for natural body movements to be captured.",
                    0
                )
            }
            
            # Get the gesture energy value
            gesture_energy_value = tabular_data.get("gesture_energy", "hands not detected")
            
            # Get feedback and score
            gesture_feedback, gesture_score = gesture_feedback_map.get(
                gesture_energy_value, ("No gesture data available.", 0)
            )

            # Convert numeric score to string for table display
            numeric_score = str(gesture_score)
            
            # Add gesture feedback to the scores
            scores_text = gesture_feedback

            # print(" I ---- > ", i - 1, midval_value)

            # Add the new row for gesture feedback to the table
            table_data.append([

                Paragraph(f"{i}.", normal_style),
                Paragraph(items_text, normal_style),
                Paragraph(numeric_score, normal_style),
                Paragraph(scores_text, normal_style)
            ])
        elif i == 4:
            # Question text
            items_text = "Did they have expression on their face?"

            # Mapping expression score (1-5) to feedback
            expression_feedback_map = {
                5: "The speaker had excellent and very positive facial expressions. This greatly enhanced the delivery and helped connect with the audience.",
                4: "The speaker showed good facial expressions, adding warmth and engagement to the talk. A bit more consistency could make it even better.",
                3: "Facial expressions were moderate. While present at times, increasing expressiveness could make the talk more dynamic.",
                2: "There was limited facial expression, which may have made the delivery feel a bit flat. Try to show more enthusiasm or emotion when appropriate.",
                1: "Facial expressions were minimal or absent. Adding expressiveness can significantly improve the impact and connection with the audience.",
                0: "No expression data available."
            }

            # Get the expression score
            expression_score = int(tabular_data.get("positive_expression_score", 0))

            # Get the corresponding feedback
            expression_feedback = expression_feedback_map.get(expression_score, "No expression data available.")
            # print(" I ---- > ", i - 1, midval_value)

            numeric_score = str(expression_score)

            # Add the new row for gesture feedback to the table
            table_data.append([

                Paragraph(f"{i}.", normal_style),
                Paragraph(items_text, normal_style),
                Paragraph(numeric_score, normal_style),
                Paragraph(expression_feedback, normal_style)
            ])
        else:
            answer_index = i if i < len(llm_answers) else None
            if answer_index is not None:
                answer = clean_answer(llm_answers[answer_index])
            else:
                answer = "N/A"
            table_data.append([
                Paragraph(f"{i}.", normal_style),
                Paragraph(question, normal_style),
                Paragraph(numeric_score, normal_style),
                Paragraph(answer, normal_style)
            ])

    # Create table with defined column widths (adjust as needed)
    table = Table(table_data, colWidths=[40, 250, 80, 200])
    table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    flowables.append(table)

    doc.build(flowables,
              onFirstPage=add_header_footer,
              onLaterPages=add_header_footer)

    print("PDF generated successfully with dynamic table!")
    # Optionally remove the temporary file if needed:
    # os.remove(save_path)

if __name__ == "__main__":
    create_combined_pdf(r"logos\logo.png", r"json\output.json", r"reports\combined_report.pdf")
