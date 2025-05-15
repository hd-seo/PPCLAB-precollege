import streamlit as st

# --- 이미지 파일 경로 (실제 파일 준비 필요) ---
IMAGE_PATH_PHARMACY = "image/pharmacy_counter.png"
IMAGE_PATH_EMERGENCY = "image/emergency_room.png"
IMAGE_PATH_DECISION_TREE = "image/simple_decision_tree.png"

# --- 세션 상태 초기화 함수 ---
def initialize_session():
    """세션 상태 변수들을 초기화합니다."""
    st.session_state.step = "start"
    st.session_state.patient_info = {"warfarin_user": None, "headache_details": None, "other_meds_checked": False}
    st.session_state.safety_score = 50 # 기본 점수
    st.session_state.consultation_history = []
    st.session_state.game_over = False
    st.session_state.action_taken_for_med_recommend = False # 약물 추천 액션을 선택했는지 여부

# --- 페이지 렌더링 함수 ---
def render_page():
    """현재 단계에 따라 페이지 내용을 렌더링합니다."""

    if "step" not in st.session_state:
        initialize_session()

    # --- 1. 시작 화면 ---
    if st.session_state.step == "start":
        st.title("💊 약물 상담 시뮬레이션: 숨겨진 단서를 찾아라!")
        try:
            st.image(IMAGE_PATH_PHARMACY, caption="약국 상담 데스크")
        except FileNotFoundError:
            st.info("[이미지: 약국 상담 데스크] 이미지를 찾을 수 없습니다. 'image' 폴더에 'pharmacy_counter.png' 파일을 넣어주세요.")
        
        st.markdown("""
        안녕하세요! 여러분은 오늘 약사의 중요한 업무 중 하나인 **'안전한 약물 상담'**을 체험하게 됩니다.
        환자에게 올바른 약을 추천하기 위해서는 마치 탐정이 사건의 단서를 찾듯, 질문을 통해 필요한 정보를 정확히 파악해야 합니다.
        
        **시나리오:** 두통을 호소하는 환자가 약국을 방문했습니다.
        """)
        if st.button("시뮬레이션 시작하기", type="primary"):
            st.session_state.step = "patient_presentation"
            st.rerun()

    # --- 2. 환자 등장 및 초기 질문 ---
    elif st.session_state.step == "patient_presentation":
        st.header("환자 방문")
        st.info("환자: 안녕하세요, 약사님. 머리가 너무 아파서 왔어요. 효과 빠른 진통제 하나 주세요.")
        st.markdown("어떤 질문으로 상담을 시작하시겠습니까?")

        question_options_1 = {
            "언제부터, 어떻게 아프기 시작했어요? (증상 구체화)": "symptom_details",
            "혹시 지금 매일 드시고 있는 다른 약이 있으세요? (복용 약물 확인)": "current_meds",
            "평소에도 머리가 자주 아프신 편인가요? (과거력 확인)": "history_headache"
        }
        chosen_question_text_1 = st.radio(
            "첫 번째 질문을 선택하세요:",
            list(question_options_1.keys()),
            key="q1_choice"
        )

        if st.button("선택한 질문하기", key="ask_q1"):
            action_1 = question_options_1[chosen_question_text_1]
            st.session_state.consultation_history.append({"type": "질문", "content": chosen_question_text_1})

            if action_1 == "current_meds":
                st.session_state.patient_info["warfarin_user"] = True
                st.session_state.patient_info["other_meds_checked"] = True
                st.session_state.safety_score += 30
                st.session_state.consultation_history.append({"type": "환자 답변", "content": "네, 의사 선생님이 처방해주셔서 '피를 묽게 하는 약(와파린)'을 매일 먹고 있어요. 심장이 좀 안 좋거든요."})
                st.success("매우 중요한 질문입니다! 환자가 '피를 묽게 하는 약(와파린)'을 복용 중임을 확인했습니다.")
                st.warning("🚨 주요 정보 확인: 환자는 '피를 묽게 하는 약(와파린)' 복용 중!")
            elif action_1 == "symptom_details":
                st.session_state.patient_info["headache_details"] = "어제 저녁부터 지끈거리며 아픔"
                st.session_state.safety_score += 5
                st.session_state.consultation_history.append({"type": "환자 답변", "content": "어제 저녁부터 지끈거리면서 아프기 시작했어요."})
                st.info("환자: 어제 저녁부터 지끈거리면서 아프기 시작했어요.")
            else: # history_headache
                st.session_state.safety_score += 5
                st.session_state.consultation_history.append({"type": "환자 답변", "content": "네, 가끔씩 스트레스 받으면 머리가 아파요."})
                st.info("환자: 네, 가끔씩 스트레스 받으면 머리가 아파요.")
            
            st.session_state.step = "action_decision"
            st.rerun()

    # --- 3. 행동 결정 단계 ---
    elif st.session_state.step == "action_decision":
        st.header("정보 확인 및 다음 행동 결정")
        st.write("현재까지 수집된 환자 정보:")
        if st.session_state.patient_info["other_meds_checked"]:
            if st.session_state.patient_info["warfarin_user"]:
                st.success("- 환자는 '피를 묽게 하는 약(와파린)'을 복용 중입니다.")
            else: # current_meds 질문을 했지만 와파린 사용자가 아닌 경우 (이 시나리오에서는 발생 안함)
                 st.info("- 환자는 현재 복용 중인 다른 약이 없다고 답변했습니다.")
        else:
            st.warning("- 환자가 다른 약을 복용 중인지 아직 확인하지 못했습니다.")
        
        if st.session_state.patient_info["headache_details"]:
            st.info(f"- 두통 증상: {st.session_state.patient_info['headache_details']}")
        
        st.markdown("어떤 행동을 하시겠습니까?")
        action_options = ["진통제 종류 선택해서 추천하기", "추가 질문하기 (다른 약 복용 여부)", "전문가(선배 약사)에게 도움 요청하기"]
        
        # 이미 다른 약 복용 여부를 확인했다면 해당 질문 옵션 제거
        if st.session_state.patient_info["other_meds_checked"]:
            action_options.remove("추가 질문하기 (다른 약 복용 여부)")
            if not action_options: # 모든 질문을 다 한 경우 (이 시나리오에서는 거의 없음)
                 action_options.append("진통제 종류 선택해서 추천하기")


        chosen_action = st.selectbox(
            "행동을 선택하세요:",
            action_options,
            key="action_choice_select"
        )

        if st.button("선택한 행동 실행하기", key="execute_action"):
            st.session_state.consultation_history.append({"type": "약사 행동", "content": chosen_action})

            if chosen_action == "진통제 종류 선택해서 추천하기":
                st.session_state.step = "drug_recommendation"
                st.session_state.action_taken_for_med_recommend = True
            elif chosen_action == "추가 질문하기 (다른 약 복용 여부)":
                # 이 선택지는 other_meds_checked가 False일 때만 나타남
                st.session_state.patient_info["warfarin_user"] = True # 시나리오상 이 질문을 하면 와파린 복용 사실을 알게 됨
                st.session_state.patient_info["other_meds_checked"] = True
                st.session_state.safety_score += 30
                st.session_state.consultation_history.append({"type": "환자 답변", "content": "네, 의사 선생님이 처방해주셔서 '피를 묽게 하는 약(와파린)'을 매일 먹고 있어요. 심장이 좀 안 좋거든요."})
                st.success("중요한 추가 질문입니다! 환자가 '피를 묽게 하는 약(와파린)'을 복용 중임을 확인했습니다.")
                st.warning("🚨 주요 정보 확인: 환자는 '피를 묽게 하는 약(와파린)' 복용 중!")
                st.session_state.step = "action_decision" # 다시 행동 결정으로 (정보 업데이트됨)
            elif chosen_action == "전문가(선배 약사)에게 도움 요청하기":
                st.session_state.safety_score += 15
                st.session_state.consultation_history.append({"type": "결과", "content": "선배 약사 도움으로 와파린 복용 사실 인지 및 안전한 약 추천."})
                st.success("현명한 판단입니다!")
                st.info("선배 약사: (환자 정보를 듣고) 아, 이 환자분은 와파린을 드시고 계실 가능성이 있겠네요. 꼭 확인하고 NSAIDs 계열 진통제는 피해야 합니다. 아세트아미노펜 성분이 더 안전하겠어요.")
                st.session_state.game_over = True
                st.session_state.step = "simulation_result"
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
            key="pk_choice_radio"
        )
        
        if st.button("이 약으로 추천하기", key="confirm_pk"):
            painkiller_type = painkiller_options[chosen_painkiller_text]
            st.session_state.consultation_history.append({"type": "약물 추천", "content": chosen_painkiller_text})

            is_warfarin_user = st.session_state.patient_info.get("warfarin_user", False)
            
            outcome_message = ""
            if is_warfarin_user and painkiller_type == "nsaids":
                st.session_state.safety_score -= 100
                outcome_message = "🚨 치명적인 실수! 환자는 '피를 묽게 하는 약(와파린)'을 복용 중이었습니다. 이 약과 소염진통제가 만나 심각한 위장출혈을 일으켜 응급실로 긴급 후송되었습니다!"
                st.error(outcome_message)
                try:
                    st.image(IMAGE_PATH_EMERGENCY, caption="응급 상황")
                except FileNotFoundError:
                    st.warning("[이미지: 응급 상황] 이미지를 찾을 수 없습니다. 'image' 폴더에 'emergency_room.png' 파일을 넣어주세요.")
            elif is_warfarin_user and painkiller_type == "acetaminophen":
                st.session_state.safety_score += 50
                outcome_message = "🎉 훌륭한 선택입니다! '피를 묽게 하는 약'을 복용 중인 환자에게 비교적 안전한 아세트아미노펜 계열 진통제를 추천하여 환자가 안전하게 회복했습니다."
                st.success(outcome_message)
                st.balloons()
            elif not is_warfarin_user and painkiller_type == "nsaids":
                # 와파린 복용 여부를 확인 안 했거나, 확인했는데 와파린 사용자가 아닌 경우 (이 시나리오에서는 전자에 해당)
                if not st.session_state.patient_info["other_meds_checked"]:
                    st.session_state.safety_score -= 20
                    outcome_message = "⚠️ 아슬아슬한 선택! 다행히 이 환자는 와파린을 복용하고 있지 않았지만, 만약 복용 중이었다면 매우 위험했을 것입니다. 환자의 다른 약물 복용 여부를 확인하는 것을 놓쳤습니다."
                    st.warning(outcome_message)
                else: # 와파린 사용자가 아님이 확인된 경우 (안전)
                    st.session_state.safety_score += 10
                    outcome_message = "적절한 선택입니다. 환자는 안전하게 증상이 호전되었습니다."
                    st.success(outcome_message)
            elif not is_warfarin_user and painkiller_type == "acetaminophen":
                st.session_state.safety_score += 10
                outcome_message = "안전한 선택입니다. 환자는 증상이 호전되었습니다."
                st.success(outcome_message)
            
            st.session_state.consultation_history.append({"type": "최종 결과", "content": outcome_message})
            st.session_state.game_over = True
            st.session_state.step = "simulation_result"
            st.rerun()

    # --- 5. 최종 결과 및 학습 포인트 ---
    elif st.session_state.step == "simulation_result" and st.session_state.game_over:
        st.header("최종 상담 결과 및 학습 포인트")

        final_outcome_entry = next((item for item in reversed(st.session_state.consultation_history) if item["type"] == "최종 결과" or "선배 약사 도움" in item["content"]), None)
        if final_outcome_entry:
            if "🚨" in final_outcome_entry["content"] or "⚠️" in final_outcome_entry["content"]:
                 st.error(f"**결과 요약:** {final_outcome_entry['content']}")
            else:
                 st.success(f"**결과 요약:** {final_outcome_entry['content']}")
        
        st.metric("나의 최종 안전 상담 점수:", st.session_state.safety_score)

        if st.session_state.safety_score >= 80: # (50 + 30 + 50) or (50 + 30 + 15)
            st.write("🌟 **평가:** 훌륭합니다! 중요한 정보를 정확히 파악하고 환자에게 안전한 선택을 했습니다.")
        elif st.session_state.safety_score >= 50: # (50 + 5 + 10) or (50 + 5 - 20)
            st.write("👍 **평가:** 잘했습니다! 몇 가지 포인트를 더 점검하면 완벽한 상담을 할 수 있을 거예요.")
        else:
            st.write("😥 **평가:** 아쉽지만, 이번 경험을 통해 중요한 것을 배웠을 것입니다. 실제 상황에서는 더 신중해야 합니다.")

        st.subheader("오늘의 상담 여정 돌아보기")
        for entry in st.session_state.consultation_history:
            if entry["type"] == "질문":
                st.markdown(f"- **[질문]** {entry['content']}")
            elif entry["type"] == "환자 답변":
                st.markdown(f"  - **[환자]** _{entry['content']}_")
            elif entry["type"] == "약사 행동":
                st.markdown(f"- **[나의 행동]** {entry['content']}")
            elif entry["type"] == "약물 추천":
                st.markdown(f"- **[약물 추천]** {entry['content']}")
            # "최종 결과"는 위에서 이미 요약했으므로 여기서는 생략 가능
        
        st.subheader("머신러닝과의 연결: 의사결정나무(Decision Tree) 이해하기")
        st.markdown("""
        오늘 여러분이 환자와 상담하며 질문하고, 답변을 얻고, 다음 행동을 결정한 과정은 머신러닝의 **'의사결정나무(Decision Tree)'** 모델이 작동하는 방식과 매우 유사합니다.
        """)
        try:
            st.image(IMAGE_PATH_DECISION_TREE, caption="간단한 의사결정나무 예시")
        except FileNotFoundError:
            st.info("[이미지: 의사결정나무] 이미지를 찾을 수 없습니다. 'image' 폴더에 'simple_decision_tree.png' 파일을 넣어주세요.")
        
        st.markdown("""
        의사결정나무는 스무고개처럼, 중요한 질문(정보)을 통해 데이터를 분류하고 예측합니다.
        - **첫 번째 질문 '지금 매일 드시는 다른 약이 있으세요?'** 는 이 나무의 중요한 **첫 번째 갈림길(분기점)**이었습니다.
        - 이 질문에 대한 답변('예' 또는 '아니오', 그리고 와파린 복용 여부)에 따라 다음 선택지와 결과가 크게 달라졌습니다.
        - 만약 이 질문을 하지 않았거나, 얻은 정보를 잘못 해석했다면 위험한 결과로 이어질 수 있었습니다.

        **머신러닝 모델은 수많은 과거 데이터를 학습하여, 어떤 질문을 어떤 순서로 하는 것이 가장 정확한 예측(또는 안전한 결정)을 하는지 스스로 규칙을 찾아냅니다.**
        마치 여러분이 이 시뮬레이션을 여러 번 반복하면서 더 나은 상담 전략을 터득하는 것과 같습니다.
        
        이처럼 데이터를 기반으로 최적의 판단 규칙을 찾아내는 것이 머신러닝의 핵심 원리 중 하나입니다.
        """)
        st.info("오늘 체험이 약물 상담의 중요성을 이해하고, 머신러닝이 우리 생활 속 문제를 어떻게 해결할 수 있는지에 대한 작은 실마리가 되었기를 바랍니다!")

        if st.button("처음부터 다시 도전하기", key="restart_sim"):
            initialize_session()
            st.rerun()

# --- 앱 실행 ---
if __name__ == "__main__":
    render_page()


'''
**코드 설명 및 주요 특징:**

* **`initialize_session()`:** 시뮬레이션 시작 또는 재시작 시 모든 상태 변수를 초기값으로 설정합니다.
* **`render_page()`:** `st.session_state.step` 값에 따라 현재 진행 단계를 구분하여 해당 UI를 표시합니다.
* **단계별 진행:** "start" -> "patient\_presentation" -> "action\_decision" -> ("drug\_recommendation") -> "simulation\_result" 순서로 진행됩니다.
* **`st.session_state.patient_info`:** 환자 관련 정보(와파린 복용 여부, 다른 약 확인 여부 등)를 저장합니다.
* **`st.session_state.safety_score`:** 학생의 선택에 따라 점수가 가감됩니다.
* **`st.session_state.consultation_history`:** 학생의 질문, 환자 답변, 약사 행동 등 주요 상호작용을 기록하여 마지막에 상담 과정을 보여줍니다.
* **위험 상황 연출:** 와파린 복용 환자에게 NSAIDs 계열 진통제를 추천하는 경우, 점수가 크게 깎이고 경고 메시지와 함께 응급실 이미지가 (있다면) 표시됩니다.
* **의사결정나무 설명:** 시뮬레이션 종료 후, 학생의 선택 과정을 의사결정나무의 분기점에 비유하여 설명하고, 머신러닝 모델이 데이터를 통해 최적의 규칙을 학습하는 원리를 간략히 소개합니다.
* **이미지 플레이스홀더:** `IMAGE_PATH_...` 변수로 이미지 경로를 지정했습니다. 실제 이미지 파일(`pharmacy_counter.png`, `emergency_room.png`, `simple_decision_tree.png`)을 코드 파일과 같은 위치의 `image` 폴더에 넣어주세요. 이미지가 없어도 텍스트 설명은 정상적으로 나옵니다.

이 Streamlit 앱을 통해 고등학생들이 약물 상담의 복잡성과 책임감을 느끼고, 동시에 데이터 기반 의사결정의 기초적인 개념을 재미있게 배울 수 있기를 바랍니다. 직접 실행해보시고, 추가적으로 수정하거나 개선하고 싶은 부분이 있다면 언제든지 알려주주세요!
'''