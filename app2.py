import streamlit as st
import random # 환자 케이스 랜덤 설정을 위해 추가

# --- 이미지 파일 경로 (실제 파일 준비 필요) ---
IMAGE_PATH_PHARMACY = "image/pharmacy_counter.png"
IMAGE_PATH_EMERGENCY = "image/emergency_room.png"
IMAGE_PATH_DECISION_TREE = "image/simple_decision_tree.png"

# --- 세션 상태 초기화 함수 ---
def initialize_session():
    """세션 상태 변수들을 초기화합니다."""
    st.session_state.step = "start"
    
    # 환자의 실제 숨겨진 상태 (게임 시작 시 고정 또는 랜덤 설정)
    # 여기서는 교육 효과를 위해 항상 위험 요인이 있도록 설정합니다.
    # 실제 사용 시에는 random.choice([True, False]) 등으로 랜덤화 가능
    st.session_state.true_patient_conditions = {
        "is_warfarin_user": True, 
        "has_implant_soon": True 
    }
    
    # 플레이어가 알게 된 정보
    st.session_state.player_discovered_info = {
        "warfarin_user_revealed": False, # 와파린 복용 사실을 알게 되었는지
        "dental_implant_revealed": False, # 임플란트 예정 사실을 알게 되었는지
        "headache_details": None,
        "headache_history_response": None,
    }
    
    # 플레이어가 각 중요 질문을 했는지 여부
    st.session_state.questions_asked_flags = {
        "symptom_details_asked": False,
        "current_meds_asked": False,
        "history_headache_asked": False,
        "medical_history_asked": False,
    }
    
    st.session_state.safety_score = 50 
    st.session_state.consultation_history = []
    st.session_state.game_over = False

# --- 페이지 렌더링 함수 ---
def render_page():
    """현재 단계에 따라 페이지 내용을 렌더링합니다."""

    if 'playthrough_count' not in st.session_state:
        st.session_state.playthrough_count = 1
    if 'missed_critical_med_question_last_time' not in st.session_state:
        st.session_state.missed_critical_med_question_last_time = False
    if 'missed_critical_history_question_last_time' not in st.session_state:
        st.session_state.missed_critical_history_question_last_time = False

    if "step" not in st.session_state:
        initialize_session()

    # --- 1. 시작 화면 ---
    if st.session_state.step == "start":
        st.title("💊 약물 상담 시뮬레이션: 숨겨진 단서를 찾아라!")
        try:
            st.image(IMAGE_PATH_PHARMACY, caption="약국 상담 데스크")
        except FileNotFoundError:
            st.info("[이미지: 약국 상담 데스크] 'image/pharmacy_counter.png' 파일을 찾을 수 없습니다.")
        
        st.markdown("""
        안녕하세요! 여러분은 오늘 약사의 중요한 업무 중 하나인 **'안전한 약물 상담'**을 체험하게 됩니다.
        환자에게 올바른 약을 추천하기 위해서는 마치 탐정이 사건의 단서를 찾듯, 질문을 통해 필요한 정보를 정확히 파악해야 합니다.
        
        **시나리오:** 두통을 호소하는 환자가 약국을 방문했습니다. (환자는 여러분이 모르는 숨겨진 건강 상태를 가지고 있을 수 있습니다!)
        """)
        if st.button("시뮬레이션 시작하기", type="primary"):
            initialize_session() 
            st.session_state.step = "patient_presentation"
            st.rerun()

    # --- 2. 환자 등장 및 초기 질문 ---
    elif st.session_state.step == "patient_presentation":
        st.header("환자 방문")
        st.markdown("### 환자:\n> 안녕하세요, 약사님. 머리가 너무 아파서 왔어요. 효과 빠른 진통제 하나 주세요.", unsafe_allow_html=True)
        
        if st.session_state.playthrough_count > 1:
            if st.session_state.missed_critical_med_question_last_time:
                st.info("💡 **힌트 (지난 상담 복기):** 환자가 현재 복용 중인 다른 약이 있는지 확인하는 것은 매우 중요합니다! 잊지 말고 질문하세요.")
            if st.session_state.missed_critical_history_question_last_time:
                st.info("💡 **힌트 (지난 상담 복기):** 환자의 다른 질병 유무나 예정된 치료/수술 계획을 확인하는 것도 안전한 상담에 큰 도움이 됩니다.")

        st.markdown("어떤 질문으로 상담을 시작하시겠습니까? (하나만 선택 가능)")

        question_options_1 = {
            "언제부터, 어떻게 아프기 시작했어요? (증상 구체화)": "symptom_details",
            "혹시 지금 매일 드시고 있는 다른 약이 있으세요? (복용 약물 확인)": "current_meds",
            "평소에도 머리가 자주 아프신 편인가요? (과거력 확인)": "history_headache",
            "혹시 다른 질병을 앓고 계시거나, 최근 또는 예정된 치과 치료/수술이 있으신가요? (병력 및 치료 계획 확인)": "medical_history_check"
        }
        
        chosen_question_text_1 = st.radio(
            "첫 번째 질문을 선택하세요:",
            list(question_options_1.keys()), # 첫 질문은 항상 모든 옵션 표시
            key="q1_choice_final_v2" 
        )

        if st.button("선택한 질문하기", key="ask_q1_final_v2"):
            action_1 = question_options_1[chosen_question_text_1]
            st.session_state.consultation_history.append({"type": "질문", "content": chosen_question_text_1})
            patient_response_text = ""

            if action_1 == "current_meds":
                st.session_state.questions_asked_flags["current_meds_asked"] = True
                if st.session_state.true_patient_conditions["is_warfarin_user"]:
                    st.session_state.player_discovered_info["warfarin_user_revealed"] = True
                    st.session_state.safety_score += 30
                    patient_response_text = "네, 의사 선생님이 처방해주셔서 '피를 묽게 하는 약(와파린)'을 매일 먹고 있어요. 심장이 좀 안 좋거든요."
                    st.success("매우 중요한 질문입니다! 환자가 '피를 묽게 하는 약(와파린)'을 복용 중임을 확인했습니다.")
                    st.warning("🚨 주요 정보 확인: 환자는 '피를 묽게 하는 약(와파린)' 복용 중!")
                else:
                    patient_response_text = "아니요, 특별히 매일 먹는 약은 없어요."
                    st.info("환자는 현재 매일 복용 중인 약이 없다고 답변했습니다.")
            elif action_1 == "symptom_details":
                st.session_state.questions_asked_flags["symptom_details_asked"] = True
                st.session_state.player_discovered_info["headache_details"] = "어제 저녁부터 지끈거리며 아픔"
                st.session_state.safety_score += 5
                patient_response_text = "어제 저녁부터 지끈거리면서 아프기 시작했어요."
            elif action_1 == "history_headache":
                st.session_state.questions_asked_flags["history_headache_asked"] = True
                st.session_state.player_discovered_info["headache_history_response"] = "가끔 스트레스 받으면 아픔"
                st.session_state.safety_score += 5
                patient_response_text = "네, 가끔씩 스트레스 받으면 머리가 아파요."
            elif action_1 == "medical_history_check":
                st.session_state.questions_asked_flags["medical_history_asked"] = True
                if st.session_state.true_patient_conditions["has_implant_soon"]:
                    st.session_state.player_discovered_info["dental_implant_revealed"] = True
                    st.session_state.safety_score += 20
                    patient_response_text = "네, 사실 다음 주에 임플란트 시술이 예정되어 있어요."
                    st.success("중요한 질문입니다! 환자의 예정된 치료 계획을 확인했습니다.")
                    st.warning("🦷 주요 정보 확인: 환자 다음 주 임플란트 시술 예정!")
                else:
                    patient_response_text = "아니요, 특별한 질병이나 예정된 치료는 없어요."
                    st.info("환자는 특별한 병력이나 치료 계획이 없다고 답변했습니다.")

            if patient_response_text:
                st.markdown(f"#### 환자:\n> {patient_response_text}", unsafe_allow_html=True)
                st.session_state.consultation_history.append({"type": "환자 답변", "content": patient_response_text})
            
            st.session_state.step = "first_question_follow_up"
            st.rerun()
            
    # --- 2.5 첫 질문 후 행동 결정 ---
    elif st.session_state.step == "first_question_follow_up":
        st.header("첫 질문 후 행동 선택")
        st.write("환자의 첫 번째 답변을 들었습니다. 다음 행동을 선택하세요:")
        
        if st.session_state.consultation_history and st.session_state.consultation_history[-1]["type"] == "환자 답변":
             st.caption(f"방금 환자 답변: \"{st.session_state.consultation_history[-1]['content']}\"")

        follow_up_options = {
            "이 정보로 바로 약물 추천하기": "go_to_drug_recommendation",
            "추가 정보 수집 및 다른 행동 고려하기": "go_to_action_decision",
            "전문가(선배 약사)에게 도움 요청하기": "ask_senior_pharmacist_early"
        }
        chosen_follow_up_text = st.radio(
            "다음 행동을 선택하세요:",
            list(follow_up_options.keys()),
            key="follow_up_choice_final_v2"
        )
        if st.button("결정", key="confirm_follow_up_final_v2"):
            action = follow_up_options[chosen_follow_up_text]
            st.session_state.consultation_history.append({"type": "약사 행동", "content": chosen_follow_up_text})

            if action == "go_to_drug_recommendation":
                st.session_state.step = "drug_recommendation"
            elif action == "go_to_action_decision":
                st.session_state.step = "action_decision"
            elif action == "ask_senior_pharmacist_early":
                st.session_state.safety_score += 15
                advice = "선배 약사: (환자 정보를 듣고) 아직 정보가 부족하지만, "
                if st.session_state.player_discovered_info.get("warfarin_user_revealed"): # 플레이어가 알게 된 정보 기준
                    advice += "와파린 복용 중이시라면 NSAIDs는 피해야 합니다. "
                if st.session_state.player_discovered_info.get("dental_implant_revealed"):
                    advice += "임플란트 예정이시면 더욱 조심해야 하고요. "
                advice += "두통 원인이나 다른 약물, 병력 등을 더 자세히 확인하는 것이 안전합니다."
                st.session_state.consultation_history.append({"type": "결과", "content": advice})
                st.success("현명한 판단입니다! 하지만 아직 정보가 부족할 수 있습니다.")
                st.markdown(f"#### 선배 약사:\n> {advice}", unsafe_allow_html=True)
                st.session_state.game_over = True 
                st.session_state.step = "simulation_result"
            st.rerun()

    # --- 3. 추가 정보 수집 및 행동 결정 단계 ---
    elif st.session_state.step == "action_decision":
        st.header("추가 정보 수집 및 행동 결정")
        st.markdown("**현재까지 내가 알게 된 환자 정보 요약:**")
        summary_texts = []
        if st.session_state.player_discovered_info["warfarin_user_revealed"]:
            summary_texts.append("와파린 복용 중")
        if st.session_state.player_discovered_info["dental_implant_revealed"]:
            summary_texts.append("다음 주 임플란트 예정")
        if st.session_state.player_discovered_info["headache_details"]:
            summary_texts.append(f"두통: {st.session_state.player_discovered_info['headache_details']}")
        if st.session_state.player_discovered_info["headache_history_response"]:
            summary_texts.append(f"두통 과거력: {st.session_state.player_discovered_info['headache_history_response']}")
        
        if summary_texts:
            for text in summary_texts:
                st.success(f"- {text}")
        else:
            st.info("- 아직 환자에 대해 알게 된 주요 정보가 없습니다.")

        st.markdown("어떤 행동을 하시겠습니까?")
        
        action_options_dict = {}
        action_options_dict["진통제 종류 선택해서 추천하기"] = "recommend_drug"
        action_options_dict["전문가(선배 약사)에게 도움 요청하기"] = "ask_senior"

        question_map = {
            "언제부터, 어떻게 아프기 시작했어요? (증상 구체화)": ("symptom_details", "symptom_details_asked"),
            "혹시 지금 매일 드시고 있는 다른 약이 있으세요? (복용 약물 확인)": ("current_meds", "current_meds_asked"),
            "평소에도 머리가 자주 아프신 편인가요? (과거력 확인)": ("history_headache", "history_headache_asked"),
            "혹시 다른 질병을 앓고 계시거나, 최근 또는 예정된 치과 치료/수술이 있으신가요? (병력 및 치료 계획 확인)": ("medical_history_check", "medical_history_asked")
        }

        for q_text, (action_key_map, asked_flag_key) in question_map.items():
            if not st.session_state.questions_asked_flags[asked_flag_key]:
                action_options_dict[f"[추가 질문] {q_text}"] = action_key_map
        
        if not any(st.session_state.questions_asked_flags[flag_key] == False for _, flag_key in question_map.values()):
            st.info("모든 주요 질문을 통해 정보를 수집한 것으로 보입니다. 이제 약물 추천 또는 전문가 상담을 고려하세요.")

        chosen_action_text = st.selectbox(
            "행동을 선택하세요:",
            list(action_options_dict.keys()),
            key="action_choice_dynamic_final_v2"
        )

        if st.button("선택한 행동 실행하기", key="execute_action_dynamic_final_v2"):
            action_key_selected = action_options_dict[chosen_action_text]
            st.session_state.consultation_history.append({"type": "약사 행동", "content": chosen_action_text})
            patient_response_text = ""

            if action_key_selected == "recommend_drug":
                st.session_state.step = "drug_recommendation"
            elif action_key_selected == "ask_senior":
                st.session_state.safety_score += 15 
                advice = "선배 약사: (환자 정보를 듣고) "
                # ... (선배 약사 조언 로직은 이전과 유사하게 player_discovered_info 기반으로) ...
                if st.session_state.player_discovered_info.get("warfarin_user_revealed") and st.session_state.player_discovered_info.get("dental_implant_revealed"):
                    advice += "와파린 복용 중이고 임플란트 예정이시군요! NSAIDs는 절대 안 됩니다. 아세트아미노펜이 안전하고, 반드시 주치의/치과의사와 와파린 조절 상담을 안내해야 합니다."
                elif st.session_state.player_discovered_info.get("warfarin_user_revealed"):
                    advice += "와파린 복용 중이시니 NSAIDs는 피하고 아세트아미노펜을 고려하세요."
                # ... (기타 조건들) ...
                else:
                    advice += "환자의 모든 정보를 종합적으로 고려하는 것이 중요합니다."
                st.session_state.consultation_history.append({"type": "결과", "content": advice})
                st.success("현명한 판단입니다!")
                st.markdown(f"#### 선배 약사:\n> {advice}", unsafe_allow_html=True)
                st.session_state.game_over = True
                st.session_state.step = "simulation_result"
            
            # 추가 질문 선택 시 로직 (첫 질문 로직과 유사하게 상세 응답 처리)
            elif action_key_selected == "current_meds":
                st.session_state.questions_asked_flags["current_meds_asked"] = True
                if st.session_state.true_patient_conditions["is_warfarin_user"]:
                    st.session_state.player_discovered_info["warfarin_user_revealed"] = True
                    st.session_state.safety_score += 30 
                    patient_response_text = "네, 아까도 말씀드렸지만 '피를 묽게 하는 약(와파린)'을 매일 먹고 있어요. 심장이 좀 안 좋거든요."
                    st.success("복용 약물 정보를 다시 확인했습니다.")
                    st.warning("🚨 주요 정보 확인: 환자는 '피를 묽게 하는 약(와파린)' 복용 중!")
                else:
                    patient_response_text = "아니요, 특별히 매일 먹는 약은 없어요."
                    st.info("환자는 현재 매일 복용 중인 약이 없다고 답변했습니다.")
            elif action_key_selected == "symptom_details":
                st.session_state.questions_asked_flags["symptom_details_asked"] = True
                st.session_state.player_discovered_info["headache_details"] = "어제 저녁부터 지끈거리며 아픔"
                st.session_state.safety_score += 5
                patient_response_text = "어제 저녁부터 지끈거리면서 아프기 시작했어요."
                st.info("증상에 대한 상세 정보를 확인했습니다.")
            elif action_key_selected == "history_headache":
                st.session_state.questions_asked_flags["history_headache_asked"] = True
                st.session_state.player_discovered_info["headache_history_response"] = "가끔 스트레스 받으면 아픔"
                st.session_state.safety_score += 5
                patient_response_text = "네, 가끔씩 스트레스 받으면 머리가 아파요."
                st.info("두통 과거력 정보를 확인했습니다.")
            elif action_key_selected == "medical_history_check":
                st.session_state.questions_asked_flags["medical_history_asked"] = True
                if st.session_state.true_patient_conditions["has_implant_soon"]:
                    st.session_state.player_discovered_info["dental_implant_revealed"] = True
                    st.session_state.safety_score += 20
                    patient_response_text = "네, 다음 주에 임플란트 시술이 예정되어 있다고 말씀드렸어요."
                    st.success("병력 및 치료 계획 정보를 다시 확인했습니다.")
                    st.warning("🦷 주요 정보 확인: 환자 다음 주 임플란트 시술 예정!")
                else:
                    patient_response_text = "아니요, 특별한 질병이나 예정된 치료는 없어요."
                    st.info("환자는 특별한 병력이나 치료 계획이 없다고 답변했습니다.")


            if patient_response_text: 
                st.markdown(f"#### 환자:\n> {patient_response_text}", unsafe_allow_html=True)
                st.session_state.consultation_history.append({"type": "환자 답변", "content": patient_response_text})
            
            if action_key_selected not in ["recommend_drug", "ask_senior"]:
                 st.session_state.step = "action_decision" 

            st.rerun()

    # --- 4. 약물 추천 단계 ---
    elif st.session_state.step == "drug_recommendation":
        st.header("진통제 추천")
        st.markdown("어떤 종류의 진통제를 추천하시겠습니까?")
        
        painkiller_options = {
            "일반 소염진통제 (성분: 이부프로펜, 나프록센 등)": "nsaids",
            "아세트아미노펜 계열 진통제 (성분: 아세트아미노펜 - 예: 타이레놀)": "acetaminophen"
        }
        chosen_painkiller_text = st.radio(
            "추천할 진통제를 선택하세요:",
            list(painkiller_options.keys()),
            key="pk_choice_radio_final_v2"
        )
        
        if st.button("이 약으로 추천하기", key="confirm_pk_final_v2"):
            painkiller_type = painkiller_options[chosen_painkiller_text]
            st.session_state.consultation_history.append({"type": "약물 추천", "content": chosen_painkiller_text})

            # 실제 환자 상태
            actual_warfarin_user = st.session_state.true_patient_conditions["is_warfarin_user"]
            actual_implant_soon = st.session_state.true_patient_conditions["has_implant_soon"]

            # 플레이어가 질문했는지 여부
            asked_about_meds = st.session_state.questions_asked_flags["current_meds_asked"]
            asked_about_history = st.session_state.questions_asked_flags["medical_history_asked"]
            
            outcome_message = ""
            score_change = 0

            if painkiller_type == "nsaids":
                if actual_warfarin_user: # 실제 와파린 복용자
                    if not asked_about_meds: # 와파린 복용자인데 안 물어봄
                        score_change = -110 
                        outcome_message = "🚨🚨🚨 치명적 상황! 환자가 알 수 없는 이유로 심각한 위장출혈을 일으켰습니다. 혹시 확인하지 않은 환자의 정보가 있었을까요?"
                        try: st.image(IMAGE_PATH_EMERGENCY, caption="응급 상황")
                        except FileNotFoundError: st.warning("[이미지 경고] 'image/emergency_room.png' 파일을 찾을 수 없습니다.")
                    else: # 와파린 복용을 (질문해서) 알고도 NSAIDs 선택
                        if actual_implant_soon: # 실제 임플란트도 예정
                            if not asked_about_history: # 임플란트 예정인데 안 물어봄 (와파린은 알고 있음)
                                 score_change = -130
                                 outcome_message = "🚨🚨🚨 최악의 상황! 와파린 복용 사실을 알면서도 NSAIDs를 선택했고, 확인하지 않은 다른 문제(임플란트)까지 겹쳐 환자가 매우 위독해졌습니다."
                            else: # 둘 다 (질문해서) 알고도 NSAIDs
                                 score_change = -120
                                 outcome_message = "🚨🚨🚨 매우 치명적인 실수! 와파린 복용 및 임플란트 시술 예정임을 알면서도 NSAIDs를 추천하여 심각한 출혈 위험을 초래했습니다!"
                        else: # 와파린만 (질문해서) 알고 NSAIDs 선택 (실제 임플란트 위험은 없음)
                            score_change = -100
                            outcome_message = "🚨🚨 치명적인 실수! 와파린 복용 사실을 알면서도 NSAIDs를 추천하여 위장출혈 위험을 크게 높였습니다!"
                        if score_change <= -100 and not ("알 수 없는 이유" in outcome_message): # 이미지가 중복되지 않도록
                            try: st.image(IMAGE_PATH_EMERGENCY, caption="응급 상황")
                            except FileNotFoundError: st.warning("[이미지 경고] 'image/emergency_room.png' 파일을 찾을 수 없습니다.")

                elif actual_implant_soon: # 실제 와파린은 안 먹지만, 임플란트 예정
                    if not asked_about_history: # 임플란트 예정인데 안 물어봄
                        score_change = -50
                        outcome_message = "⚠️ 위험! 환자가 시술 후 예상치 못한 출혈 문제로 고생했습니다. 예정된 시술이 있는지 확인했어야 합니다."
                    else: # 임플란트 예정 (질문해서) 알고도 NSAIDs
                        score_change = -40
                        outcome_message = "⚠️ 주의! 임플란트 시술 예정임을 알면서도 NSAIDs를 추천했습니다. 출혈 경향을 높일 수 있습니다."
                else: # 실제 위험 요인 없음 (와파린X, 임플란트X)
                    if not asked_about_meds and not asked_about_history:
                        score_change = -10 
                        outcome_message = "다행히 환자에게 특이사항은 없었지만, 다른 약물 복용 여부와 병력/치료 계획을 모두 확인하는 것이 안전합니다."
                    elif not asked_about_meds:
                        score_change = -5
                        outcome_message = "다행히 환자에게 특이사항은 없었지만, 다른 약물 복용 여부를 확인하는 것이 안전합니다."
                    elif not asked_about_history:
                        score_change = -5
                        outcome_message = "다행히 환자에게 특이사항은 없었지만, 병력/치료 계획을 확인하는 것이 안전합니다."
                    else: 
                        score_change = 10
                        outcome_message = "적절한 선택으로 보입니다. 환자는 증상 완화에 도움을 받을 수 있습니다."
            
            elif painkiller_type == "acetaminophen": 
                score_change = 10 
                outcome_message = "안전한 선택입니다. 환자는 증상이 호전될 수 있습니다."
                additional_advice_needed = False

                if actual_warfarin_user:
                    if not asked_about_meds:
                        outcome_message += " (하지만, 환자가 실제 와파린 복용 중이라는 사실을 확인하지 못한 점은 매우 아쉽습니다. 우연히 안전한 약을 골랐습니다.)"
                        score_change -= 5 # 큰 위험은 피했지만, 정보 누락 감점
                    elif actual_implant_soon: # 와파린O, 임플란트O, 둘 다 물어봄
                         if asked_about_history:
                            score_change = 25 
                            outcome_message = "🎉 최선의 선택! 와파린 복용 및 임플란트 예정 환자에게 아세트아미노펜을 추천하고, 필요한 추가 상담 안내까지 고려하면 완벽합니다."
                            additional_advice_needed = True
                            st.balloons()
                         else: # 와파린O, 임플란트O, 와파린만 물어봄
                            outcome_message += " (환자의 임플란트 계획을 확인하지 않은 점은 아쉽습니다.)"
                            score_change +=5 # 와파린 인지하고 아세트아미노펜은 좋은 선택
                elif actual_implant_soon:
                    if not asked_about_history:
                        outcome_message += " (하지만, 환자의 임플란트 계획을 확인하지 못한 점은 아쉽습니다.)"
                        score_change -= 3
                    else: # 임플란트 알고 아세트아미노펜
                        score_change = 15
                        outcome_message = "안전한 약물 선택입니다. 임플란트 시술 관련해서는 치과의사와 상담하도록 안내하면 좋습니다."
                        additional_advice_needed = True
                
                if additional_advice_needed and "🎉" in outcome_message : # 최선의 경우에만 풍선
                    pass # 이미 풍선 띄움
                elif additional_advice_needed:
                     st.info("💡 추가 조언: 환자에게 주치의 또는 치과의사와의 상담을 권유하는 것이 좋습니다.")


            st.session_state.safety_score += score_change
            
            if score_change < -50 : st.error(outcome_message)
            elif score_change < 0 : st.warning(outcome_message)
            else: st.success(outcome_message)
            
            st.session_state.consultation_history.append({"type": "최종 결과", "content": outcome_message, "score_change": score_change})
            st.session_state.game_over = True
            st.session_state.step = "simulation_result"
            st.rerun()

    # --- 5. 시뮬레이션 결과 (게임 한 판 종료) ---
    elif st.session_state.step == "simulation_result" and st.session_state.game_over:
        st.header("상담 결과")
        st.metric("나의 최종 안전 상담 점수:", st.session_state.safety_score)

        if st.session_state.safety_score >= 80: 
            st.write("🌟 **평가:** 훌륭합니다! 중요한 정보를 정확히 파악하고 환자에게 안전한 선택을 했습니다.")
        elif st.session_state.safety_score >= 50: 
            st.write("👍 **평가:** 잘했습니다! 몇 가지 포인트를 더 점검하면 완벽한 상담을 할 수 있을 거예요.")
        else:
            st.write("😥 **평가:** 아쉽지만, 이번 경험을 통해 중요한 것을 배웠을 것입니다. 실제 상황에서는 더 신중해야 합니다.")

        # 다음 플레이를 위한 힌트 플래그 설정
        # 실제 위험이 있었는데 해당 질문을 안 해서 나쁜 결과가 나왔을 경우 힌트 활성화
        if st.session_state.true_patient_conditions["is_warfarin_user"] and \
           not st.session_state.questions_asked_flags["current_meds_asked"] and \
           st.session_state.safety_score < 50: # 점수 기준은 상황에 맞게 조절
            st.session_state.missed_critical_med_question_last_time = True
        else:
            st.session_state.missed_critical_med_question_last_time = False
        
        if st.session_state.true_patient_conditions["has_implant_soon"] and \
           not st.session_state.questions_asked_flags["medical_history_asked"] and \
           st.session_state.safety_score < 50:
            st.session_state.missed_critical_history_question_last_time = True
        else:
            st.session_state.missed_critical_history_question_last_time = False

        st.subheader("오늘의 상담 여정 돌아보기")
        for entry in st.session_state.consultation_history:
            if entry["type"] == "질문":
                st.markdown(f"- **[질문]** {entry['content']}")
            elif entry["type"] == "환자 답변":
                 # 환자 답변 스타일 강화
                st.markdown(f"  - <div style='font-size: 1.1em; margin-left: 20px;'><b>[환자]</b> 🗣️ <i>{entry['content']}</i></div>", unsafe_allow_html=True)
            elif entry["type"] == "약사 행동":
                st.markdown(f"- **[나의 행동]** {entry['content']}")
            elif entry["type"] == "약물 추천":
                st.markdown(f"- **[약물 추천]** {entry['content']}")
            elif entry["type"] == "최종 결과":
                 st.markdown(f"- **[결과]** {entry['content']} (점수 변동: {entry.get('score_change',0)})")
            elif "선배 약사" in entry["content"]: 
                 st.markdown(f"- <div style='font-size: 1.1em; margin-left: 20px;'><b>[선배 약사]</b> 🧑‍⚕️ <i>{entry['content'].replace('선배 약사: (환자 정보를 듣고)','')}</i></div>", unsafe_allow_html=True)

        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("처음부터 다시 도전하기", key="restart_game_final_v2"):
                st.session_state.playthrough_count += 1 
                initialize_session() 
                st.session_state.step = "patient_presentation" 
                st.rerun()
        with col2:
            if st.button("학습 내용 정리 보기 및 시뮬레이션 종료", key="view_summary_and_exit_final_v2"):
                st.session_state.step = "final_summary"
                st.rerun()
                
    # --- 6. 최종 학습 정리 페이지 ---
    elif st.session_state.step == "final_summary":
        st.header("학습 내용 정리: 머신러닝과의 연결")
        # ... (이전과 동일한 내용) ...
        st.markdown("""
        여러 번의 시뮬레이션을 통해 환자 상담 과정을 경험해보셨습니다. 
        이러한 상담 과정은 머신러닝의 **'의사결정나무(Decision Tree)'** 모델이 작동하는 방식과 매우 유사합니다.
        """)
        try:
            st.image(IMAGE_PATH_DECISION_TREE, caption="간단한 의사결정나무 예시")
        except FileNotFoundError:
            st.info("[이미지: 의사결정나무] 'image/simple_decision_tree.png' 파일을 찾을 수 없습니다.")
        
        st.markdown("""
        의사결정나무는 스무고개처럼, 중요한 질문(정보)을 통해 데이터를 분류하고 예측합니다.
        - **상담 중 했던 질문들 ('다른 약 복용 여부', '다른 질병/치료 계획 여부' 등)** 은 이 나무의 중요한 **갈림길(분기점)**이었습니다. 이 질문에 대한 답변, 또는 질문을 했는지 여부 자체가 중요한 판단 기준이 되었습니다.
        - 환자의 실제 숨겨진 상태(예: 와파린 복용, 임플란트 예정)를 파악하기 위한 적절한 질문을 하지 않으면, 마치 의사결정나무가 중요한 특징(feature)을 사용하지 못해 잘못된 예측을 하는 것과 같습니다.
        - 최적의 약물 선택은 환자의 모든 관련 정보를 고려해야 하며, 누락된 정보는 예기치 않은 위험으로 이어질 수 있습니다.

        **머신러닝 모델은 수많은 과거 데이터를 학습하여, 어떤 질문을 어떤 순서로 하는 것이 가장 정확한 예측(또는 안전한 결정)을 하는지 스스로 규칙을 찾아냅니다.**
        마치 여러분이 이 시뮬레이션을 여러 번 반복하면서 (그리고 때로는 힌트를 얻으면서) 더 나은 상담 전략을 터득하는 것과 같습니다. 
        첫 시도에서 중요한 정보를 놓쳤더라도 ('환자가 알 수 없는 이유로 위독해짐'), 다음 시도에서는 그 경험을 바탕으로 더 나은 질문을 할 수 있게 되는 것처럼, 머신러닝도 반복적인 학습과 피드백을 통해 성능을 개선합니다.
        
        이처럼 데이터를 기반으로 최적의 판단 규칙을 찾아내는 것이 머신러닝의 핵심 원리 중 하나입니다.
        """)
        st.info("오늘 체험이 약물 상담의 중요성을 이해하고, 머신러닝이 우리 생활 속 문제를 어떻게 해결할 수 있는지에 대한 작은 실마리가 되었기를 바랍니다!")

        if st.button("새로운 시뮬레이션 세션 시작하기 (모든 기록 초기화)", key="restart_new_session_final_v2"):
            keys_to_delete = list(st.session_state.keys())
            for key in keys_to_delete:
                del st.session_state[key]
            st.rerun()

# --- 앱 실행 ---
if __name__ == "__main__":
    render_page()
