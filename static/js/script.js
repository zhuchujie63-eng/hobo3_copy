document.addEventListener("DOMContentLoaded", () => {
    // Translations
    const translations = {
        en: {
            app_title: "SpaceTranslator v2.0",
            app_subtitle: "Explore the Galaxy of Languages",
            mode1_title: "English Input",
            mode1_desc: "To CN + Foreign + Audio",
            mode3_title: "English Voiceover",
            mode3_desc: "Direct TTS, no translation",
            mode2_title: "Chinese Input",
            mode2_desc: "To Foreign + Audio",
            mode5_title: "Video Tools",
            mode5_desc: "Download & Process",
            input_placeholder_en: "Enter English text...",
            input_placeholder_cn: "Please enter Chinese text...",
            input_placeholder_tiktok: "Please paste TikTok video link here...",
            process_btn: "Generate",
            process_btn_tiktok: "Extract Subtitles",
            load_video_btn: "Load Video",
            target_lang_label: "Target Language:",
            history_title: "History",
            clear_history: "Clear All",
            no_history: "No history yet",
            history_btn: "History",
            sub_title: "Upgrade Plan",
            plan_free: "Free",
            feat_limit: "5 Credits / Month",
            feat_basic: "Basic Translation",
            feat_tts: "Standard TTS",
            current_plan: "Current Plan",
            plan_pro: "Pro",
            feat_unlimited: "Unlimited Access",
            feat_fast: "Priority Processing",
            feat_premium: "Premium Support",
            btn_upgrade: "Upgrade Now",
            recommended: "Recommended",
            result_title: "Result",
            audio_title: "Audio Output",
            btn_dl_cn_srt: "Download Chinese SRT",
            btn_dl_target_srt: "Download Target SRT",
            coop_btn: "Cooperation",
            faq_btn: "FAQ",
            feedback_btn: "Feedback",
            coop_title: "Cooperation",
            scan_qr: "Scan QR Code to add WeChat",
            faq_title: "FAQ & Tutorial",
            feedback_title: "Feedback",
            feedback_desc: "We value your suggestions. Please let us know how we can improve.",
            submit_btn: "Submit Feedback",
            feedback_success: "Thank you for your feedback!",
            logout_btn: "Logout"
        },
        zh: {
            app_title: "星际翻译官 v2.0",
            app_subtitle: "探索语言的浩瀚星河",
            mode1_title: "英文输入",
            mode1_desc: "转中文 + 外语 + 配音",
            mode3_title: "英文配音",
            mode3_desc: "英文文案直接配音，不进行翻译",
            mode2_title: "中文输入",
            mode2_desc: "转外语 + 配音",
            mode5_title: "视频工具",
            mode5_desc: "下载与处理",
            input_placeholder_en: "请输入英文文本...",
            input_placeholder_cn: "请输入中文文案...",
            input_placeholder_tiktok: "在此粘贴 TikTok 视频链接...",
            process_btn: "开始生成",
            process_btn_tiktok: "提取字幕",
            load_video_btn: "加载视频",
            target_lang_label: "目标语言：",
            history_title: "历史记录",
            clear_history: "清空历史",
            no_history: "暂无历史记录",
            history_btn: "历史",
            sub_title: "升级套餐",
            plan_free: "免费版",
            feat_limit: "每月 5 个积分",
            feat_basic: "基础翻译功能",
            feat_tts: "标准语音合成",
            current_plan: "当前套餐",
            plan_pro: "专业版",
            feat_unlimited: "无限畅享",
            feat_fast: "优先处理",
            feat_premium: "专属客服支持",
            btn_upgrade: "立即升级",
            recommended: "推荐",
            result_title: "处理结果",
            audio_title: "语音输出",
            btn_dl_cn_srt: "下载中文字幕",
            btn_dl_target_srt: "下载外语字幕",
            coop_btn: "商务合作",
            faq_btn: "常见问题",
            feedback_btn: "问题反馈",
            coop_title: "商务合作",
            scan_qr: "扫码添加微信",
            faq_title: "新手教程与常见问题",
            feedback_title: "问题反馈",
            feedback_desc: "我们非常重视您的建议，请告诉我们要如何改进。",
            submit_btn: "提交反馈",
            feedback_success: "感谢您的反馈！",
            logout_btn: "退出登录"
        }
    };

    const modeOptions = document.querySelectorAll(".mode-option");

    // Header & Language Elements
    const uiLangBtn = document.getElementById("ui-lang-btn");
    const uiLangMenu = document.getElementById("ui-lang-menu");
    const currentLangText = document.getElementById("current-lang-text");
    const langOptions = document.querySelectorAll(".lang-option");

    // History Drawer Elements
    const historyToggleBtn = document.getElementById("history-toggle-btn");
    const historyDrawer = document.getElementById("history-drawer");
    const historyOverlay = document.getElementById("history-overlay");
    const closeHistoryBtn = document.getElementById("close-history-btn");
    const secondLangSelector = document.getElementById("second-lang-selector");
    const pureModeOptions = document.getElementById("pure-mode-options");
    const inputText = document.getElementById("input-text");
    const translationInputArea = inputText.closest(".input-area");
    
    const charCount = document.querySelector(".char-count");
    const processBtn = document.getElementById("process-btn");
    const processBtnArea = processBtn.closest(".action-area");
    
    const resultArea = document.getElementById("result-area");
    const translationOutput = document.getElementById("translation-output");
    const audioContainer = document.getElementById("audio-container");
    const audioPlayer = document.getElementById("audio-player");
    const downloadCnSrtBtn = document.getElementById("download-cn-srt-btn");
    const downloadTargetSrtBtn = document.getElementById("download-target-srt-btn");
    const statusMsg = document.getElementById("status-msg");

    // History Elements
    const historyList = document.getElementById("history-list");
    const clearHistoryBtn = document.getElementById("clear-history-btn");

    // Video Downloader Elements
    const videoDownloaderArea = document.getElementById("video-downloader-area");
    const videoUrlInput = document.getElementById("video-url-input");
    const loadVideoBtn = document.getElementById("load-video-btn");
    const iframeId = "#cardApiIframe";

    // TikTok Result Elements
    const tiktokResultArea = document.getElementById("tiktok-result-area");
    const tiktokPreview = document.querySelector(".tiktok-preview");
    const tiktokThumbnail = document.getElementById("tiktok-thumbnail");
    const tiktokVideoPlayer = document.getElementById("tiktok-video-player");
    const tiktokTitle = document.getElementById("tiktok-title");
    const tiktokLangSelect = document.getElementById("tiktok-lang-select");
    const timestampToggle = document.getElementById("timestamp-toggle");
    const tiktokCopyBtn = document.getElementById("tiktok-copy-btn");
    const tiktokDownloadBtn = document.getElementById("tiktok-download-btn");
    const tiktokSubtitleText = document.getElementById("tiktok-subtitle-text");
    
    let tiktokData = null; // Store fetched data

    // Subscription & Credits Logic
    const subStatusBtn = document.getElementById("sub-status-btn");
    const subModal = document.getElementById("sub-modal");
    const closeSubModalBtn = document.getElementById("close-sub-modal");
    const upgradeBtn = document.getElementById("upgrade-btn");
    const headerCreditCount = document.getElementById("header-credit-count");
    const subBadge = document.querySelector(".sub-badge");
    const subText = document.querySelector(".sub-text");

    let userCredits = parseInt(localStorage.getItem("userCredits") || "5");
    let isPro = localStorage.getItem("isPro") === "true";
    
    // Check if it's a new month to reset credits (Simple check)
    const lastReset = localStorage.getItem("lastResetDate");
    const currentMonth = new Date().getMonth();
    
    if (!lastReset || new Date(lastReset).getMonth() !== currentMonth) {
        if (!isPro) {
            userCredits = 5;
            localStorage.setItem("userCredits", "5");
        }
        localStorage.setItem("lastResetDate", new Date().toISOString());
    }

    function updateSubUI() {
        const lang = localStorage.getItem("uiLanguage") || "en";
        if (isPro) {
            subBadge.classList.remove("free");
            subBadge.classList.add("pro");
            subText.textContent = "Pro";
            headerCreditCount.innerHTML = '<i class="fa-solid fa-infinity"></i>';
            document.querySelector(".plan-card.free-plan .current-plan-badge").style.display = "none";
            
            // Add current plan badge to pro plan if not exists
            if (!document.querySelector(".plan-card.pro-plan .current-plan-badge")) {
                const badge = document.createElement("div");
                badge.className = "current-plan-badge";
                badge.setAttribute("data-i18n", "current_plan");
                badge.textContent = translations[lang].current_plan;
                document.querySelector(".plan-card.pro-plan").appendChild(badge);
                document.querySelector(".plan-card.pro-plan #upgrade-btn").style.display = "none";
            }
        } else {
            subBadge.classList.remove("pro");
            subBadge.classList.add("free");
            subText.textContent = translations[lang].plan_free;
            headerCreditCount.textContent = `${userCredits}/5`;
        }
    }

    function checkCredits(cost = 1) {
        if (isPro) return true;
        if (userCredits >= cost) {
            return true;
        } else {
            subModal.classList.remove("hidden");
            return false;
        }
    }

    function deductCredits(cost = 1) {
        if (isPro) return;
        userCredits = Math.max(0, userCredits - cost);
        localStorage.setItem("userCredits", userCredits);
        updateSubUI();
    }

    // Event Listeners for Subscription
    subStatusBtn.addEventListener("click", () => {
        subModal.classList.remove("hidden");
    });

    closeSubModalBtn.addEventListener("click", () => {
        subModal.classList.add("hidden");
    });

    subModal.addEventListener("click", (e) => {
        if (e.target === subModal) {
            subModal.classList.add("hidden");
        }
    });

    upgradeBtn.addEventListener("click", () => {
        const originalText = upgradeBtn.textContent;
        upgradeBtn.textContent = "Processing...";
        upgradeBtn.disabled = true;

        // Simulate payment processing
        setTimeout(() => {
            isPro = true;
            localStorage.setItem("isPro", "true");
            updateSubUI();
            subModal.classList.add("hidden");
            alert("Upgrade Successful! You now have unlimited access.");
            upgradeBtn.textContent = originalText;
            upgradeBtn.disabled = false;
        }, 1500);
    });

    // Initialize UI
    updateSubUI();

    // Theme Toggle Logic
    const themeToggleBtn = document.getElementById("theme-toggle");
    const themeIcon = themeToggleBtn.querySelector("i");
    
    // Check saved theme - Default to 'light' for now to match CSS, but user can toggle
    // Actually, Space theme implies dark default, but let's respect saved pref.
    const savedTheme = localStorage.getItem("theme") || "light";
    document.documentElement.setAttribute("data-theme", savedTheme);
    updateThemeIcon(savedTheme);

    themeToggleBtn.addEventListener("click", () => {
        const currentTheme = document.documentElement.getAttribute("data-theme");
        const newTheme = currentTheme === "dark" ? "light" : "dark";
        
        document.documentElement.setAttribute("data-theme", newTheme);
        localStorage.setItem("theme", newTheme);
        updateThemeIcon(newTheme);
    });

    function updateThemeIcon(theme) {
        if (theme === "dark") {
            themeIcon.classList.remove("fa-moon");
            themeIcon.classList.add("fa-sun");
        } else {
            themeIcon.classList.remove("fa-sun");
            themeIcon.classList.add("fa-moon");
        }
    }

    let currentMode = "1";

    // Mode Selection Logic
    modeOptions.forEach(option => {
        option.addEventListener("click", () => {
            modeOptions.forEach(opt => opt.classList.remove("active"));
            option.classList.add("active");
            currentMode = option.dataset.mode;
            updateUIForMode(currentMode);
        });
    });

    function updateUIForMode(mode) {
        // Reset visibility
        secondLangSelector.style.display = "none";
        if (pureModeOptions) pureModeOptions.style.display = "none"; // Might be removed in HTML, keeping safe check
        videoDownloaderArea.style.display = "none";
        
        // Hide TikTok Result Area
        if (tiktokResultArea) tiktokResultArea.classList.add("hidden");
        if (resultArea) resultArea.classList.add("hidden");
        
        // Show Translation UI by default
        translationInputArea.style.display = "block";
        processBtnArea.style.display = "flex";

        // Language Options Visibility
        const optEnglish = document.getElementById("lang-option-english");
        const optFrench = document.getElementById("lang-option-french");
        const optGerman = document.getElementById("lang-option-german");
        const optPortuguese = document.getElementById("lang-option-portuguese");
        const optJapanese = document.getElementById("lang-option-japanese");

        // Reset all to visible (default state logic)
        if (optEnglish) optEnglish.style.display = "inline-block";
        if (optFrench) optFrench.style.display = "inline-block";
        if (optGerman) optGerman.style.display = "inline-block";
        if (optPortuguese) optPortuguese.style.display = "inline-block";
        if (optJapanese) optJapanese.style.display = "inline-block";

        if (mode === "5") {
            translationInputArea.style.display = "none";
            processBtnArea.style.display = "none";
            resultArea.classList.add("hidden");
            
            // Show Video UI
            videoDownloaderArea.style.display = "block";
            return;
        }

        if (mode === "4") {
            const lang = localStorage.getItem("uiLanguage") || "en";
            inputText.placeholder = translations[lang].input_placeholder_tiktok || "Please paste TikTok link...";
            processBtn.querySelector(".btn-text").textContent = translations[lang].process_btn_tiktok || "Extract Subtitles";
            // Hide second language selector
            secondLangSelector.style.display = "none";
            return;
        } else {
             // Reset Process Button Text
             const lang = localStorage.getItem("uiLanguage") || "en";
             processBtn.querySelector(".btn-text").textContent = translations[lang].process_btn;
        }

        if (mode === "1") {
            secondLangSelector.style.display = "block";
            const lang = localStorage.getItem("uiLanguage") || "en";
            inputText.placeholder = translations[lang].input_placeholder_en;
            
            // Hide English option (source is English)
            if (optEnglish) optEnglish.style.display = "none";
            
            // Ensure a valid option is checked if current check is hidden
            const checked = document.querySelector("input[name='second_lang']:checked");
            if (checked && checked.value === "English") {
                 const fr = document.querySelector("input[name='second_lang'][value='French']");
                 if (fr) fr.checked = true;
            }

        } else if (mode === "2") {
            secondLangSelector.style.display = "block";
            const lang = localStorage.getItem("uiLanguage") || "en";
            inputText.placeholder = translations[lang].input_placeholder_cn;
            
            // Show English, Hide Japanese (unless requested, but usually CN->JP is separate or user didn't ask)
            if (optEnglish) optEnglish.style.display = "inline-block";
            if (optJapanese) optJapanese.style.display = "none";

            // If JP was selected, switch to English or French
            const checked = document.querySelector("input[name='second_lang']:checked");
            if (checked && checked.value === "Japanese") {
                 const en = document.querySelector("input[name='second_lang'][value='English']");
                 if (en) en.checked = true;
            }
        } else if (mode === "3") {
            const lang = localStorage.getItem("uiLanguage") || "en";
            inputText.placeholder = translations[lang].input_placeholder_en;
        }
    }

    // Character Count
    inputText.addEventListener("input", () => {
        const length = inputText.value.length;
        charCount.textContent = `${length} chars`;
    });

    // Process Button Click
    processBtn.addEventListener("click", async () => {
        // Check Credits
        if (!checkCredits(1)) return;

        const text = inputText.value.trim();
        if (!text) {
            alert("Please enter some text.");
            return;
        }

        // Set Loading State
        processBtn.classList.add("loading");
        processBtn.disabled = true;
        resultArea.classList.add("hidden");
        audioContainer.classList.add("hidden");
        statusMsg.textContent = "Processing...";

        // Prepare Payload
        const payload = {
            text: text,
            mode: currentMode,
            enable_tts: true // Always enable TTS now that Mode 4 is gone
        };
        const voiceSelectEl = document.getElementById("voice-select");
        if (voiceSelectEl) {
            payload.voice_id = voiceSelectEl.value;
        }

        if (currentMode === "1" || currentMode === "2") {
            const selectedLang = document.querySelector("input[name='second_lang']:checked").value;
            payload.second_lang = selectedLang;
        }

        try {
            const response = await fetch("/api/process", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            });

            const ct = (response.headers.get("content-type") || "").toLowerCase();
            let data;
            if (ct.includes("application/json")) {
                data = await response.json();
            } else {
                const text = await response.text();
                if (response.redirected || text.includes("登录") || text.includes("Login")) {
                    throw new Error("需要登录，请重新登录后再试");
                }
                throw new Error("服务返回了非 JSON 响应");
            }

            if (response.ok) {
                // Mode 4 Handling
                if (currentMode === "4" && data.subtitles) {
                    tiktokData = data;
                    renderTikTokUI();
                    tiktokResultArea.classList.remove("hidden");
                    statusMsg.textContent = "Done!";
                    
                    // Deduct Credits
                    deductCredits(1);
                    return;
                }

                translationOutput.textContent = data.translation;
                resultArea.classList.remove("hidden");
                statusMsg.textContent = "Done!";
                
                // Audio Handling
                if (data.audio_url) {
                    audioPlayer.src = data.audio_url;
                    audioContainer.classList.remove("hidden");
                } else {
                    audioContainer.classList.add("hidden");
                }
                
                // Reset buttons
                downloadCnSrtBtn.style.display = "none";
                downloadTargetSrtBtn.style.display = "none";
                
                if (data.cn_srt_url) {
                    downloadCnSrtBtn.href = data.cn_srt_url;
                    downloadCnSrtBtn.style.display = "inline-block";
                }
                if (data.target_srt_url) {
                    downloadTargetSrtBtn.href = data.target_srt_url;
                    downloadTargetSrtBtn.style.display = "inline-block";
                    
                    // Custom text for Mode 4
                    if (currentMode === "4") {
                        downloadTargetSrtBtn.textContent = "Download SRT";
                    } else {
                         const lang = localStorage.getItem("uiLanguage") || "en";
                         downloadTargetSrtBtn.textContent = translations[lang].btn_dl_target_srt;
                    }
                }

                // Deduct Credits
                deductCredits(1);

                // Save to History
                saveHistory(text, data.translation);

            } else {
                statusMsg.textContent = "Error: " + (data.error || "Unknown error");
                alert("Error: " + (data.error || "Unknown error"));
            }

        } catch (error) {
            console.error("Error:", error);
            statusMsg.textContent = "Error: " + (error && error.message ? error.message : "Network error");
            alert(error && error.message ? error.message : "Network error occurred.");
        } finally {
            processBtn.classList.remove("loading");
            processBtn.disabled = false;
        }
    });

    // Synthesize Button Click
    const synthesizeBtn = document.getElementById("synthesize-btn");
    const voiceSelect = document.getElementById("voice-select");

    if (synthesizeBtn) {
        synthesizeBtn.addEventListener("click", async () => {
            if (!checkCredits(1)) return;

            const textToSynthesize = translationOutput.textContent;
            if (!textToSynthesize) {
                alert("No text to synthesize.");
                return;
            }

            const voiceId = voiceSelect.value;

            synthesizeBtn.classList.add("loading");
            synthesizeBtn.disabled = true;
            statusMsg.textContent = "Synthesizing audio...";

            try {
                const response = await fetch("/api/synthesize", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ text: textToSynthesize, voice_id: voiceId })
                });

                const data = await response.json();

                if (response.ok) {
                    audioPlayer.src = data.audio_url;
                    audioPlayer.play();
                    audioContainer.classList.remove("hidden");
                    statusMsg.textContent = "Audio ready!";
                    deductCredits(1);
                } else {
                    throw new Error(data.error || "Failed to generate audio.");
                }
            } catch (error) {
                console.error("Synthesis Error:", error);
                statusMsg.textContent = `Error: ${error.message}`;
                alert(error.message);
            } finally {
                synthesizeBtn.classList.remove("loading");
                synthesizeBtn.disabled = false;
            }
        });
    }

    // TikTok Logic
    const langMap = {
        "eng-us": "英语 (美国)",
        "eng": "英语",
        "cmn-hans-cn": "中文 (简体)",
        "cmn-hant-cn": "中文 (繁体)",
        "fra-fr": "法语",
        "deu-de": "德语",
        "jpn-jp": "日语",
        "kor-kr": "韩语",
        "spa-es": "西班牙语",
        "ita-it": "意大利语",
        "rus-ru": "俄语",
        "por-br": "葡萄牙语 (巴西)",
        "ind-id": "印尼语",
        "vie-vn": "越南语",
        "tha-th": "泰语",
        "msa-my": "马来语",
        "fil-ph": "菲律宾语",
        "tur-tr": "土耳其语",
        "ara-sa": "阿拉伯语",
        "nld-nl": "荷兰语",
        "pol-pl": "波兰语",
        "swe-se": "瑞典语",
        "dan-dk": "丹麦语",
        "fin-fi": "芬兰语",
        "nor-no": "挪威语",
        "ces-cz": "捷克语",
        "hun-hu": "匈牙利语",
        "ron-ro": "罗马尼亚语",
        "ukr-ua": "乌克兰语",
        "ell-gr": "希腊语",
        "heb-il": "希伯来语",
        "cat-es": "加泰罗尼亚语",
        "hin-in": "印地语",
        "ben-in": "孟加拉语"
    };

    function getLangName(code) {
        if (!code) return "Unknown";
        const lower = code.toLowerCase();
        // Exact match
        if (langMap[lower]) return langMap[lower];
        
        // Try splitting by dash (e.g. "eng-gb" -> "eng")
        const part = lower.split('-')[0];
        if (langMap[part]) return langMap[part] + ` (${code})`;
        
        return code.toUpperCase();
    }

    function renderTikTokUI() {
        if (!tiktokData) return;
        
        // Reset Video Player
        if (tiktokVideoPlayer) {
            tiktokVideoPlayer.pause();
            tiktokVideoPlayer.currentTime = 0;
            tiktokVideoPlayer.src = "";
            tiktokVideoPlayer.classList.add("hidden");
            if (tiktokPreview) tiktokPreview.classList.remove("playing");
        }

        // 1. Metadata
        if (tiktokData.metadata) {
            tiktokThumbnail.src = tiktokData.metadata.thumbnail || "";
            tiktokTitle.textContent = tiktokData.metadata.title || "TikTok Video";
            tiktokTitle.title = tiktokData.metadata.title || "";
            
            // Setup Video Player
            if (tiktokData.metadata.video_url && tiktokVideoPlayer) {
                // TikTok video URLs often need a proxy or direct fetch to work due to Referer checks
                // For now, we try direct link. If it fails, user still has thumbnail.
                tiktokVideoPlayer.src = tiktokData.metadata.video_url;
                
                // Click to play
                if (tiktokPreview) {
                    tiktokPreview.onclick = () => {
                        tiktokPreview.classList.add("playing");
                        tiktokVideoPlayer.classList.remove("hidden");
                        tiktokVideoPlayer.play().catch(e => {
                            console.error("Play failed", e);
                            // Fallback if direct play fails (likely CORS/Referer)
                            alert("Unable to play video directly due to TikTok restrictions. Please verify with thumbnail.");
                        });
                    };
                }
            } else {
                 if (tiktokPreview) tiktokPreview.onclick = null;
            }
        }
        
        // 2. Language Select
        tiktokLangSelect.innerHTML = "";
        tiktokData.subtitles.forEach((sub, index) => {
            const option = document.createElement("option");
            option.value = sub.lang;
            option.textContent = getLangName(sub.lang); 
            tiktokLangSelect.appendChild(option);
        });
        
        // Select first by default
        if (tiktokLangSelect.options.length > 0) {
            tiktokLangSelect.selectedIndex = 0;
        }
        
        // 3. Render Content
        updateTikTokContent();
    }
    
    function updateTikTokContent() {
        if (!tiktokData) return;
        
        const selectedLang = tiktokLangSelect.value;
        const showTimestamp = timestampToggle.checked;
        
        const sub = tiktokData.subtitles.find(s => s.lang === selectedLang);
        if (sub) {
            let content = sub.content;
            if (!showTimestamp) {
                // Remove timestamps (00:00:00,000 --> 00:00:00,000) and indices
                // Simple regex to strip standard SRT format
                // Remove timestamps lines
                content = content.replace(/\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}.*?\n/g, "");
                // Remove index numbers (lines that are just numbers)
                content = content.replace(/^\d+\s*$/gm, "");
                // Remove empty lines multiple times
                content = content.replace(/\n\s*\n/g, "\n");
            }
            tiktokSubtitleText.value = content.trim();
            
            // Update Download Link
            const blob = new Blob([content], { type: "text/plain" });
            const url = URL.createObjectURL(blob);
            tiktokDownloadBtn.href = url;
            const ext = showTimestamp ? "srt" : "txt";
            tiktokDownloadBtn.download = `tiktok_${selectedLang}.${ext}`;
        }
    }
    
    if (tiktokLangSelect) {
        tiktokLangSelect.addEventListener("change", updateTikTokContent);
    }
    
    if (timestampToggle) {
        timestampToggle.addEventListener("change", updateTikTokContent);
    }
    
    if (tiktokCopyBtn) {
        tiktokCopyBtn.addEventListener("click", () => {
            tiktokSubtitleText.select();
            document.execCommand("copy"); // Legacy but widely supported, or use Clipboard API
            
            const icon = tiktokCopyBtn.querySelector("i");
            icon.classList.remove("fa-copy");
            icon.classList.add("fa-check");
            setTimeout(() => {
                icon.classList.remove("fa-check");
                icon.classList.add("fa-copy");
            }, 2000);
        });
    }

    // Video Downloader Logic
    loadVideoBtn.addEventListener("click", () => {
        // Check Credits
        if (!checkCredits(1)) return;

        const url = videoUrlInput.value.trim();
        if (url) {
            const videoIframe = document.querySelector(iframeId);
            // New API format
            videoIframe.src = `https://p.savenow.to/api/card2/?url=${url}&adUrl=https://myAdurl.com`;
            // Deduct Credits immediately for video load (simplified)
            deductCredits(1);
        } else {
            alert("Please enter a valid URL");
        }
    });

    // --- New Modals Logic (Cooperation, FAQ, Feedback) ---
    
    // Cooperation
    const coopBtn = document.getElementById("coop-btn");
    const coopModal = document.getElementById("coop-modal");
    const closeCoopBtn = document.getElementById("close-coop-modal");
    
    if (coopBtn && coopModal) {
        coopBtn.addEventListener("click", () => coopModal.classList.remove("hidden"));
        if (closeCoopBtn) closeCoopBtn.addEventListener("click", () => coopModal.classList.add("hidden"));
        coopModal.addEventListener("click", (e) => {
            if (e.target === coopModal) coopModal.classList.add("hidden");
        });
    }

    // FAQ
    const faqBtn = document.getElementById("faq-btn");
    const faqModal = document.getElementById("faq-modal");
    const closeFaqBtn = document.getElementById("close-faq-modal");

    if (faqBtn && faqModal) {
        faqBtn.addEventListener("click", () => faqModal.classList.remove("hidden"));
        if (closeFaqBtn) closeFaqBtn.addEventListener("click", () => faqModal.classList.add("hidden"));
        faqModal.addEventListener("click", (e) => {
            if (e.target === faqModal) faqModal.classList.add("hidden");
        });
    }

    // Feedback
    const feedbackBtn = document.getElementById("feedback-btn");
    const feedbackModal = document.getElementById("feedback-modal");
    const closeFeedbackBtn = document.getElementById("close-feedback-modal");
    const submitFeedbackBtn = document.getElementById("submit-feedback-btn");
    const feedbackInput = document.getElementById("feedback-input");

    if (feedbackBtn && feedbackModal) {
        feedbackBtn.addEventListener("click", () => feedbackModal.classList.remove("hidden"));
        
        const closeFeedback = () => {
            feedbackModal.classList.add("hidden");
            if (feedbackInput) feedbackInput.value = ""; 
        };

        if (closeFeedbackBtn) closeFeedbackBtn.addEventListener("click", closeFeedback);
        feedbackModal.addEventListener("click", (e) => {
            if (e.target === feedbackModal) closeFeedback();
        });

        if (submitFeedbackBtn) {
            submitFeedbackBtn.addEventListener("click", () => {
                const text = feedbackInput.value.trim();
                if (text) {
                    const lang = localStorage.getItem("uiLanguage") || "en";
                    alert(translations[lang].feedback_success || "Thank you!");
                    feedbackInput.value = "";
                    feedbackModal.classList.add("hidden");
                } else {
                    alert("Please enter some feedback.");
                }
            });
        }
    }

    // --- History Logic ---

    function loadHistory() {
        const history = JSON.parse(localStorage.getItem("translationHistory") || "[]");
        historyList.innerHTML = "";

        if (history.length === 0) {
            const lang = localStorage.getItem("uiLanguage") || "en";
            const msg = translations[lang].no_history;
            historyList.innerHTML = `<div class="history-item" style="text-align: center; color: var(--text-secondary); cursor: default;" data-i18n="no_history">${msg}</div>`;
            return;
        }

        history.forEach((item, index) => {
            const div = document.createElement("div");
            div.className = "history-item";
            div.innerHTML = `
                <div class="history-text" title="${item.source}">${item.source}</div>
                <div class="history-meta">
                    <span>${new Date(item.timestamp).toLocaleTimeString()}</span>
                    <span>${item.lang || ''}</span>
                </div>
            `;
            div.addEventListener("click", () => {
                inputText.value = item.source;
                translationOutput.textContent = item.result;
                resultArea.classList.remove("hidden");
                audioContainer.classList.add("hidden"); // Hide audio for history recall as we don't store audio URL persistence guaranteed
                charCount.textContent = `${item.source.length} chars`;
            });
            historyList.appendChild(div);
        });
    }

    function saveHistory(source, result) {
        let history = JSON.parse(localStorage.getItem("translationHistory") || "[]");
        
        // Get current language
        let lang = "";
        const langRadio = document.querySelector("input[name='second_lang']:checked");
        if (langRadio && secondLangSelector.style.display !== "none") {
            lang = langRadio.value;
        }

        const newItem = {
            source: source,
            result: result,
            lang: lang,
            timestamp: Date.now()
        };

        // Add to beginning
        history.unshift(newItem);

        // Limit to 20 items
        if (history.length > 20) {
            history = history.slice(0, 20);
        }

        localStorage.setItem("translationHistory", JSON.stringify(history));
        loadHistory();
    }

    clearHistoryBtn.addEventListener("click", () => {
        if (confirm("Clear all history?")) {
            localStorage.removeItem("translationHistory");
            loadHistory();
        }
    });

    // --- Language Switching Logic ---

    // Toggle Dropdown
    if (uiLangBtn) {
        uiLangBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            uiLangMenu.classList.toggle("hidden");
        });
    }

    // Close Dropdown when clicking outside
    document.addEventListener("click", (e) => {
        if (uiLangBtn && !uiLangBtn.contains(e.target)) {
            uiLangMenu.classList.add("hidden");
        }
    });

    // Language Selection
    langOptions.forEach(option => {
        option.addEventListener("click", () => {
            const lang = option.dataset.lang;
            setLanguage(lang);
            uiLangMenu.classList.add("hidden");
        });
    });

    function setLanguage(lang) {
        localStorage.setItem("uiLanguage", lang);
        
        // Update Active State
        langOptions.forEach(opt => {
            if (opt.dataset.lang === lang) opt.classList.add("active");
            else opt.classList.remove("active");
        });

        // Update Button Text
        if (currentLangText) {
            currentLangText.textContent = lang === "en" ? "EN" : "CN";
            if (lang === "zh") currentLangText.textContent = "CN";
        }

        // Update Text Content
        document.querySelectorAll("[data-i18n]").forEach(el => {
            const key = el.getAttribute("data-i18n");
            if (translations[lang][key]) {
                el.textContent = translations[lang][key];
            }
        });

        // Update Placeholders
        updateInputPlaceholder(lang);
        
        // Update Sub UI text (Free/Pro badge)
        updateSubUI();
    }

    function updateInputPlaceholder(lang) {
        if (!lang) lang = localStorage.getItem("uiLanguage") || "en";
        
        if (currentMode === "1") {
            inputText.placeholder = translations[lang].input_placeholder_en;
        } else if (currentMode === "2") {
            inputText.placeholder = translations[lang].input_placeholder_cn;
        } else if (currentMode === "3") {
            inputText.placeholder = translations[lang].input_placeholder_en;
        }
    }

    // --- History Drawer Logic ---

    function openHistory() {
        historyDrawer.classList.add("open");
        historyOverlay.classList.remove("hidden");
        setTimeout(() => historyOverlay.classList.add("open"), 10);
    }

    function closeHistory() {
        historyDrawer.classList.remove("open");
        historyOverlay.classList.remove("open");
        setTimeout(() => historyOverlay.classList.add("hidden"), 300);
    }

    if (historyToggleBtn) historyToggleBtn.addEventListener("click", openHistory);
    if (closeHistoryBtn) closeHistoryBtn.addEventListener("click", closeHistory);
    if (historyOverlay) historyOverlay.addEventListener("click", closeHistory);

    // Initialize Language
    const savedLang = localStorage.getItem("uiLanguage") || "zh";
    setLanguage(savedLang);

    // Initialize History
    loadHistory();
});
