# Actions
ACTIONS = [START, SELECTING_TRACK_ACTION, SELECTING_ENGINEERING, SELECTING_DATA_SCIENCE,
           SELECTING_MANAGEMENT, SELECTING_MARKETING, SELECTING_QA] \
    = list(map(str, range(7)))

# Different users
IAM_NEW_USER, IAM_OLD_USER = map(str, range(7, 9))

SELECT_TRACK_FROM_START = str(9)

TRACKS_SET = [TRACK_ENGINEERING, TRACK_DS, TRACK_MANAGEMENT, TRACK_MARKETING,
              TRACK_QA, SELECT_TRACK_NEXT, RETURN_TO_SELECT_TRACK] \
    = list(map(str, range(10, 17)))

TRACK_ENGINEERING_SET = [ENGIN_JAVA, ENGIN_PY, ENGIN_CSH, ENGIN_IOS, ENGIN_ANDROID, ENGIN_CPP,
                         ENGIN_GO, ENGIN_RUBY, ENGIN_PHP, ENGIN_JS_FRONT, ENGIN_JS_BACK,
                         ENGIN_DEVOPS] \
    = list(map(str, range(17, 29)))

TRACK_DS_SET = [DS_ANALYST, DS_ENGINEER, DS_SIMP_ANALYST, DS_ML_ENGINEER, DS_ML_RESEARCHER] \
    = list(map(str, range(29, 34)))

TRACK_MANAGEMENT_SET = [MANAGEMENT_PRODUCT, MANAGEMENT_PROJECT, MANAGEMENT_TECH, MANAGEMENT_AGILE,
                        MANAGEMENT_HR] \
    = list(map(str, range(34, 39)))

TRACK_MARKETING_SET = [MARKETING_INTERNET, MARKETING_PR, MARKETING_EVENT, MARKETING_BRANDING,
                       MARKETING_COMMUNITY, MARKETING_SMM, MARKETING_ADV, MARKETING_CONTENT] \
    = list(map(str, range(39, 47)))

TRACK_SIMPLE_SET = [TRACK_DESIGN] = list(map(str, range(47, 48)))

TRACK_QA_SET = [QA_AUTO, QA_MANUAL] = list(map(str, range(48, 50)))

SELECT_COMPANY, SELECT_COMPANY_NEXT, SELECTING_COMPANY_ACTION = map(str, range(50, 53))
