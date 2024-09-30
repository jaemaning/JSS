import subprocess
import sys
import os
import json


def install(package : str) -> None:
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
def save_to_json(data, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    
def save_to_text(data, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        for d in data:
            for q, a in d.items():
                file.write(q + ":" + '\n\n' + a + "\n\n")

def save_to_text_one(data, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write("\n\n" + data + "\n\n")

# 직무 관련 정리 클래스
class Job:
    company_name : str = None
    job_name : str = None
    job_desc : str = None
    news : list = []
    
    def get_all(self):
        return f"""
            지원 회사명 : {self.company_name}
            지원 직무명 : {self.job_name}
            ----------------------------------
            지원 직무기술서 : 
            {self.job_desc}
            
            ----------------------------------
            지원 회사 & 직무 관련 뉴스 기사 :
            {",\n\n".join(news for news in self.news)}
            """
    
    def set_company_name(self, val):
        self.company_name = val
        return self.get_all()
    
    def set_job_name(self, val):
        self.job_name = val
        return self.get_all()
    
    def set_job_desc(self, val):
        self.job_desc = val
        return self.get_all()
    
    def add_news(self, val):
        self.news.append(val)
        return self.get_all()
    
    def pop_news(self, idx):
        if len(self.news) <= idx:
            raise IndexError(f"현재 저장된 뉴스 기사는 {len(self.news)}개 입니다. 삭제할 데이터의 번호를 {len(self.news)-1} 이하로 설정하세요.")
        self.news.pop(idx)
        return self.get_all()
    
    def init_all(self):
        self.company_name = None
        self.job_name = None
        self.job_desc = None
        self.news = []
        return self.get_all()

# 나의 경험 정리용 클래스 : Singleton
class Exp:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Exp, cls).__new__(cls)
            cls._instance.my_exp = []
            cls._instance.about_me = ""
        return cls._instance
    
    def get_exp(self):
        return self.my_exp
    
    def add_exp(self, content : str):
        self.my_exp.append(content)
        return self.my_exp
        
    def update_exp(self, target_index : int, content: str):
        if target_index >= len(self.my_exp):
            if len(self.my_exp) != 0:
                raise IndexError(f"너의 경험은 총 {len(self.my_exp)}개 입니다. 수정할 데이터의 번호를 {len(self.my_exp)-1} 이하로 설정하세요.")
            else:
                raise ValueError("현재 경험이 없습니다. 경험을 추가 후에 수정하세요.")
        else:
            self.my_exp[target_index] = content
            return self.my_exp
    
    def remove_exp(self, target_index :int):
        if target_index >= len(self.my_exp):
            if len(self.my_exp) != 0:
                raise IndexError(f"너의 경험은 총 {len(self.my_exp)}개 입니다. 삭제할 데이터의 번호를 {len(self.my_exp)-1} 이하로 설정하세요.")
            else:
                raise ValueError("현재 경험이 없습니다. 삭제가 불가능합니다.")
        else:
            del self.my_exp[target_index]
            return self.my_exp
        
    def get_about_me(self):
        return self.about_me
        
    def set_about_me(self, val):
        self.about_me = val
        return self.about_me
        

# 자소서 생성 객체 구현
class JSS:
    '''
    #####
    변수설명
    
    api_key : api 키 직접입력 or .env 파일 정의된 apikey 변수명
    useEnv : True(.env 사용 안함) / False(.env 사용)
    
    #####
    '''
    gptAPIKey : str  # GPT API 키 저장 
    client : object  # openAI 연결 인스턴스
    response = []  # 최종 응답 답변을 저장
    job : Job  # 직무 관련 정보 인스턴스
    exp : Exp  # 내 경험 작성 인스턴스
    questions = []  # 자소서 질문 -> [ 질문, max_len, t값(true or false), 프로젝트인덱스 ]
    model = "gpt-4o-mini-2024-07-18"  # 기본 사용 모델 변경가능
    
    def __init__(self, api_key: str, useEnv=False, modelName=None):
        if useEnv:
            try:
                from dotenv import load_dotenv, find_dotenv
            except:
                install('python-dotenv')
                from dotenv import load_dotenv, find_dotenv

            load_dotenv(find_dotenv())
            self.gptAPIKey = os.getenv(api_key)
        else:
            self.gptAPIKey = api_key
        
        # openai Import
        try:
            import openai
        except:
            install('openai')
            import openai
        
        if not self.gptAPIKey:
            raise ValueError("GPT API Key를 찾을 수 없습니다.")
        
        if modelName:
            self.model = os.getenv(modelName)
        
        self.client = openai.OpenAI(api_key=self.gptAPIKey)
        self.exp = Exp()
        self.job = Job()

    # 경험관리 부분
    def get_my_exp(self) -> list:
        return self.exp.get_exp()
    
    def set_my_exp(self, content: str, *idx: int):
        if idx:
            return self.exp.update_exp(target_index=idx[0],content=content)
        else:
            return self.exp.add_exp(content=content)
    
    def remove_my_exp(self, idx: int):
        return self.exp.remove_exp(target_index=idx)
    
    def set_achivement(self, val: str) -> str:
        self.exp.set_achivement(val)
        return self.exp.get_achivement()
    
    # 직무관리 부분
    def get_job_all(self):
        return self.job.get_all()
    
    def set_company_name(self, val : str):
        return self.job.set_company_name(val)
        
    def set_job_name(self, val : str):
        return self.job.set_job_name(val)
        
    def set_job_desc(self, val: str):
        return self.job.set_job_desc(val)
    
    def add_news(self, val: str):
        return self.job.add_news(val)
    
    def pop_new(self, idx: int):
        return self.job.pop_news(idx)
    
    def init_job(self):
        return self.job.init_all()
    
    '''
    
    기업 맞춤 자소서 생성 함수 - 예시 자소서 질문
    
    ex) OO기업 모바일앱/웹 서비스를 사용해 본 경험과 BigTech 기업의 플랫폼과 비교하여 강점 및 개선점에 대해 서술해 주세요.
    ex) OO기업 OO 사업부의 OO 직무에 지원한 동기를 작성해 주세요.
    
    '''
    def jss_for_company(self, question, max_length):
        prompt = f"""
        제공된 회사명과 직무 이름, 직무 설명, 회사 최근 뉴스 정보를 바탕으로 다음 자기소개서 질문의 답변을 작성하세요.
        나의 정보에 대해서 거짓없이 작성하고 너무 과도한 추측을 통해 글을 작성하지 않도록 주의합니다.
        
        **자기소개서 질문:**
        {question}
        
        **회사명:**
        {self.job.company_name}

        **직무 이름:**
        {self.job.job_name}

        **직무 설명:**
        {self.job.job_desc}
        
        **회사 최근 뉴스 정보:**
        {self.job.news}

        회사의 최근 뉴스와 직무 설명을 기반으로 자기소개서 질문에 맞게 작성하세요.:
        - 자기소개서 질문에 대한 답변임을 항상 생각하고 연관성을 고려하여 작성해야합니다.
        - 회사명과 직무 이름을 기입할 경우 제공된 회사명, 직무 이름으로 작성하세요.
        - 되도록 간결하게 작성하며, 기회에 대해 전문적이고 열정적인 어조를 유지하세요.
        """
        
        res = jss.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": f"너는 {self.job.company_name}라는 회사 {self.job.job_name} 직무에 지원한 입사지원자라고 생각하고 회사에서 제시한 자기소개서 질문인 {question} 에 대한 답변을 성실히 수행합니다. 글자수는 {max_length}자를 넘지 않도록 유의하여 작성합니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            top_p=0.1
        )
        
        answer = res.choices[0].message.content
        
        return answer
        
        
    '''
    
    나의 경험 맞춤 자소서 생성 함수 - 예시 자소서 질문
    
    ex) OO기업 모바일앱/웹 프론트엔드 개발팀에 기여할 수 있는 자신의 기술을 서술하세요.
    ex) OO기업 OO직무와 관련된 경험을 토대로 본인이 적합한 사유를 서술하세요.
    
    '''
    def jss_for_experience(self, question, max_length, *val):
        if not val:
            val = range(1, len(self.exp.get_exp()) + 1)  # 만약 val 값이 없으면 모든 경험을 선택
            
        prompt = f"""
        제공된 회사명과 직무 이름, 나의 경험, 나의 프로젝트, 나의 성과를 바탕으로 다음 자기소개서 질문의 답변을 작성하세요.
        나의 정보에 대해서 거짓없이 작성하고 너무 과도한 추측을 통해 글을 작성하지 않도록 주의합니다.

        **나의 개인 정보: **
        {self.exp.about_me}
        
        **자기소개서 질문:**
        {question}
        
        **회사명:**
        {self.job.company_name}

        **직무 이름:**
        {self.job.job_name}

        **직무 설명:**
        {self.job.job_desc}
        
        **나의 경험 및 프로젝트:**
        {"".join(self.exp.get_exp()[i-1] for i in val if isinstance(i, int))}


        나의 경험, 나의 프로젝트, 나의 성과를 기반으로 자기소개서 질문에 맞게 작성하세요.:
        - 자기소개서 질문에 대한 답변임을 항상 생각하고 연관성을 고려하여 작성해야합니다.
        - 회사명과 직무 이름을 기입할 경우 제공된 회사명, 직무 이름으로 작성하세요.
        - 되도록 간결하게 작성하며, 기회에 대해 전문적이고 열정적인 어조를 유지하세요.
        - 나의 경험과 기술이 직무 설명과 일치하는 부분을 찾아 강조하세요.
        - 직무 설명과 관련된 주요 성취와 기여를 강조하세요.
        - 되도록 간결하게 작성하며, 기회에 대해 전문적이고 열정적인 어조를 유지하세요.
        """

        res = jss.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": f"너는 {self.job.company_name}라는 회사 {self.job.job_name} 직무에 지원한 입사지원자라고 생각하고 회사에서 제시한 자기소개서 질문인 {question} 에 대한 답변을 성실히 수행합니다. 글자수는 {max_length}자를 넘지 않도록 유의하여 작성합니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            top_p=0.1
        )
        
        answer = res.choices[0].message.content
        
        return answer
    
    def run(self, questions):
        self.questions = questions
        
        # t == true 일때 내 경험 토대 자소서 생성
        for question, max_len, t, project_idx in questions:
            if t:
                ans = self.jss_for_experience(question, max_len, project_idx)
            else:
                ans = self.jss_for_company(question, max_len)

            self.response.append({question : ans + f"\n\n글자수 : {len(ans)} / {max_len}글자"})
            
        return self.response
    
    def otherRun(self, question, example, max_length):
        prompt = f"""
        다음 아래 예시 글을 토대로 {question} 질문에 답변을 작성해봐
        
        {example}
        
        - 글자수는 {max_length} 를 넘지않게 작성해줘
        """

        res = jss.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": f"너는 {self.job.company_name}라는 회사 {self.job.job_name} 직무에 지원한 입사지원자라고 생각하고 회사에서 제시한 자기소개서 질문인 {question} 에 대한 답변을 성실히 수행합니다. 글자수는 {max_length}자를 넘지 않도록 유의하여 작성합니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            top_p=0.1
        )
        
        answer = res.choices[0].message.content
        
        return answer
    
    def __repr__(self):
        return str(self.response)
        
        
if __name__ == "__main__":
    jss = JSS("GPT_SECRET_KEY", useEnv=True, modelName="MODEL")
    
    with open("./data/exp.json", 'r', encoding="utf-8") as file:
        my_exp = json.load(file)
        for e in my_exp['my_project']:
            jss.exp.add_exp(e)
        jss.exp.set_about_me(my_exp['about_me'])
    
    # 예시용 데이터로 실제 2024 - 자소설 닷컴 기준 LG전자 직무 기술서를 참고하여 작성하였습니다.
    lgJss = JSS("GPT_SECRET_KEY", useEnv=True, modelName="MODEL")
    print(lgJss.exp.get_exp())
    print(lgJss.exp)
    
    
    company_name = "LG 전자"
    job_name = "BS사업부"
    job_desc = """
    새로운 도전을 꿈꾸시는 여러분 안녕하세요.
    BS사업본부는 '버티컬별 고객 맞춤형 솔루션 Provider'로서 LG전자의 우수한 제품과 솔루션을 기업고객에게 제안하여, 고객가치 향상을 지원하고 고객과 함께 성장하는 진정한 사업파트너를 지향하고 있습니다.
    SW공학 직무에선 디스플레이 제품을 구매하는 고객들의 요구를 충족시키기 위해 최신 webOS 기술과 전문 지식을 활용한 제품과 솔루션을 개발하고 있어요. 고객의 요구를 충족시키기 위해 제품 개발에 대한 전략을 수립하고 이를 실천하기 위한 업무를 지원하며, 팀 간의 업무를 고려하여 개발 정책을 구상하여 이를 제품 개발 프로세스에 적용해 개발의 효율성을 높입니다. 또한 개발실 내 조직들이 원활하게 협업할 수 있도록 전략을 수립하고, 개발에 필요한 가이드라인을 제안하며 소프트웨어 플랫폼의 중장기 로드맵을 고민하고 설계하여 보안 프로세스를 정립해 제품의 안정성을 확보하고 있어요.
    글로벌 시장을 선도하기 위하여 많은 우수인재를 모시고 있어요. 관련 프로젝트 경험이 없더라도 다양한 직무 교육 프로그램을 통해 충분히 업무를 수행하실 수 있고, 고객의 더 나은 미래 공간을 만드는 즐거운 변화에 동참하고 싶은 인재라면 누구든지 환영해요. 저희 BS사업본부의 SW공학 직무에서 큰 꿈을 함께 이루어 나가실 수 있도록 적극 지원할게요.
    
    SW Architecture
    webOS 선행 플랫폼 설계 프로세스 정립 및 개발
    선행 기술 개발 및 유관 부서와의 협력을 통해 기술적 과제 진행
    제품 및 기술 개발을 위한 중장기 전략을 수립
    
    이러한 경험/역량이 있으신 분과 함께 하고 싶어요
    C, C++, Shell, Python을 활용한 개발 경험이 있으신 분
    프로젝트 리딩 및 여러 사람과 협업 경험이 있는 분
    해외연구소와 영어로 업무 진행이 가능하신 분
    추가로 이런 경험/역량이 있으면 더 좋아요
    성장하는 기술 분야에서 열의를 가지고 자신의 커리어를 만들어가고 싶으신 분
    유관 전공의 석사 이상 학위 소지자
    애자일 SW개발 개발 경험
    SW 플랫폼 아키텍쳐에 관심이 많으신 분
    적극적인 성격으로 문제를 해결하려고 하는 성향
    """
    news = f"""
    {company_name}과 관련된 긍정적이고 기술적인 뉴스 기사, {company_name} CEO 신년사를 검색해서 찾아보고 이를 바탕으로 아래 자기소개서 항목을
    작성하는데 사용해줘
    """
    # 5가지 자소서 항목 작성
    # 질문 / 글자수 / 내경험맞춤(True) or 회사 맞춤(False) / 내 경험 프로젝트 중 몇번째 프로젝트와 연관되어 작성할지 인덱스 (복수 선택 가능)
    questions = [
        ["지원동기 : LG전자에 대한 지원동기에 대하여 구체적으로 기술하여 주십시오.", 1000, False, (0,)],
        ["My Future : 본인의 직무관련 경험과 강점에 기반한 향후계획에 대하여 본인의 경험에 기반하여 직무관련 본인의 강점과 경쟁력이 무엇인지 구체적으로 적고, 이를 바탕으로 입사 후 활용될 수 있는 부분과 향후계획에 대해 구체적으로 기술해주시기 바랍니다", 1000, True, (1,2)],
    ]
    
    LG_jss = JSS("GPT_SECRET_KEY", useEnv=True, modelName="MODEL")
    LG_jss.set_company_name(company_name)
    LG_jss.set_job_name(job_name)
    LG_jss.set_job_desc(job_desc)
    LG_jss.add_news(news)
    
    # # 질문 넣고 동작
    ans = LG_jss.run(questions)
    
    save_to_text(ans, "./output/LG_jss_answer.txt")
    
    # json 형태로 저장
    # save_to_json(ans, "./output/LG_jss_answer_basic.json")
    # txt 형태로 저장
    # save_to_text(ans, "./output/LG_jss_answer_basic.txt")

    