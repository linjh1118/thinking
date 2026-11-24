import{a as e,d as t,f as n,p as r,r as i,t as a,u as o,v as s}from"./src-DdQX6Gcb.js";var c=n(),l=s(r(),1),u=o();function d(e){let t={a:`a`,em:`em`,h2:`h2`,h3:`h3`,h4:`h4`,img:`img`,li:`li`,p:`p`,strong:`strong`,ul:`ul`,...e.components};return(0,u.jsxs)(u.Fragment,{children:[(0,u.jsxs)(t.p,{children:[`Over the past three months, we have aggressively scaled both loop depth and model size in parallel. The first surprise came from the `,(0,u.jsx)(t.strong,{children:`Loop Transformer`}),` architecture itself. By executing a shared block of layers across multiple iterations, the model can reason more deeply without adding parameters, effectively matching the performance of much larger models.`]}),`
`,(0,u.jsxs)(t.ul,{children:[`
`,(0,u.jsxs)(t.li,{children:[`
`,(0,u.jsxs)(t.p,{children:[(0,u.jsx)(t.strong,{children:`GLM-5.4`}),` is our first flagship model built on the Loop Transformer architecture, reaching intelligence levels comparable to 2T-3T parameter models.`]}),`
`]}),`
`,(0,u.jsxs)(t.li,{children:[`
`,(0,u.jsxs)(t.p,{children:[(0,u.jsx)(t.strong,{children:`GLM-5.4`}),` marks the start of `,(0,u.jsx)(t.strong,{children:`Generalized Coding`}),`, where code becomes the foundation for solving a much wider range of tasks and unlocking new capabilities.`]}),`
`]}),`
`]}),`
`,(0,u.jsx)(t.p,{children:`The model still has some limitations. Most notably, it tends to get caught in overly long "marathon thinking" loops, though this prolonged reflection and self-correction does consistently improve accuracy beyond its parameter count.`}),`
`,(0,u.jsx)(t.h2,{children:`The Loop Architecture`}),`
`,(0,u.jsx)(t.p,{children:(0,u.jsx)(t.img,{src:`https://z-ai-bj.oss-cn-beijing.aliyuncs.com/prompts-rich-media-resources/5.4-blog/image.png`,alt:``})}),`
`,(0,u.jsx)(t.p,{children:`As we noted in our GLM-5.3 technical blog, memory-intensive tasks benefit from more parameters, while reasoning-intensive tasks benefit from more effective compute. Large-scale software engineering, cybersecurity, 3D modeling, and physical control are all ultra-long-chain reasoning tasks. The model must follow multi-step causal chains while maintaining global logical consistency. Stacking parameters and memorizing data cannot solve this.`}),`
`,(0,u.jsx)(t.h3,{children:`From Pre-Trained Base to Loop Transformer`}),`
`,(0,u.jsx)(t.p,{children:`In a standard Transformer, each layer runs once per forward pass. In a Loop Transformer, a group of weight-shared layers runs for multiple iterations, refining the hidden states from the previous pass. This gives us a deeper network without increasing the parameter count.`}),`
`,(0,u.jsx)(t.p,{children:`The idea is not new. The 2018 Universal Transformer proposed weight-shared depth, and recent work on recurrent depth and looped language models has shown gains at small scales. However, while weight sharing improves parameter efficiency, looped models trained from scratch still lag behind unshared models under the same pre-training compute budget. Instead of pre-training from scratch, we adapted an already pre-trained base model into a Loop Transformer through continued training. This lets us raise the intelligence ceiling with a relatively small compute overhead.`}),`
`,(0,u.jsx)(t.h3,{children:`Architectural Modifications at 750B Scale`}),`
`,(0,u.jsx)(t.p,{children:`GLM-5.4 loops 28 layers of the GLM-5 base model for two iterations. To balance performance gains with deployment costs at the 750B scale, we made three changes after extensive experimentation:`}),`
`,(0,u.jsx)(t.h4,{children:(0,u.jsx)(t.strong,{children:`Gated Progressive Updates`})}),`
`,(0,u.jsx)(t.p,{children:`When converting middle layers of an existing model into a multi-pass loop, directly overwriting hidden states causes activation norms to blow up across iterations. Downstream layers then receive representations outside their expected scale and distribution.`}),`
`,(0,u.jsx)(t.p,{children:`GLM-5.4 adds independent per-token gates for each iteration to proportionally write candidate updates back into the residual stream. After training, these gates develop a clear division of labor. The first pass builds global context and writes conservatively with small gate values to keep scales stable. The second pass reuses this state to refine the output, opening the gates to write full updates. The gates also adjust step size dynamically based on token difficulty: on harder tokens, the first pass writes more aggressively so complex predictions benefit more from iterative refinement.`}),`
`,(0,u.jsx)(t.h4,{children:(0,u.jsx)(t.strong,{children:`Hybrid KV Cache (Global Sharing + Independent Sliding Window)`})}),`
`,(0,u.jsx)(t.p,{children:`A naive implementation keeps a full KV cache for every loop iteration, multiplying memory usage with the loop count. Instead, we build on cross-loop KV sharing by supplementing it with a local sliding window for the new pass: the second loop reuses the sparse KV selected in the first pass, while retaining its own newly generated KV within the sliding window. These two KV streams can overlap at the same positions, allowing the model to attend to both the first-pass context representations and the updated local representations from the second pass.`}),`
`,(0,u.jsx)(t.p,{children:`As a result, an extra loop only costs one sliding window of KV cache rather than a full context cache. At 1M context lengths, this keeps GLM-5.4’s deployment cost increase over GLM-5.3 well under control.`}),`
`,(0,u.jsx)(t.h4,{children:(0,u.jsx)(t.strong,{children:`Sparse Attention Index Reuse`})}),`
`,(0,u.jsx)(t.p,{children:`GLM-5.4’s base model uses sparse attention. The second loop directly reuses the attention indices generated by the first loop's indexer, adding zero indexing overhead. Our experiments show this performs nearly identically to recomputing indices on every pass.`}),`
`,(0,u.jsx)(t.h3,{children:`Scaling Correctness & Controlled Iso-Parameter Ablations`}),`
`,(0,u.jsxs)(t.p,{children:[`Looping is also a strict test of `,(0,u.jsx)(t.strong,{children:`Scaling Correctness`}),`: any architectural change must still work at scale. Before committing our flagship model to it, we validated the Loop architecture progressively across 1B, 4B, 30B, and 750B base models.`]}),`
`,(0,u.jsx)(t.p,{children:`On a 30B model with the exact same architecture as our 750B base, we ran a controlled iso-parameter comparison. With identical parameter counts and only ~10% more total training compute, the looped version showed clear gains:`}),`
`,(0,u.jsx)(t.p,{children:(0,u.jsx)(t.img,{src:`https://z-ai-bj.oss-cn-beijing.aliyuncs.com/prompts-rich-media-resources/5.4-blog/img_v3_0217n_2d1a655c-5bce-4b3f-9115-2ad7c397ce5g.png`,alt:``})}),`
`,(0,u.jsx)(t.p,{children:(0,u.jsx)(t.em,{children:`(Evaluated on the 30B model after 200K long-context SFT, with thinking mode enabled.)`})}),`
`,(0,u.jsx)(t.p,{children:`Two findings stand out:`}),`
`,(0,u.jsxs)(t.ul,{children:[`
`,(0,u.jsxs)(t.li,{children:[`
`,(0,u.jsxs)(t.p,{children:[(0,u.jsx)(t.strong,{children:`Longer reasoning chains benefit more.`}),` The largest gains show up in math, scientific reasoning, and long-context tasks, which are core to Generalized Coding.`]}),`
`]}),`
`,(0,u.jsxs)(t.li,{children:[`
`,(0,u.jsxs)(t.p,{children:[(0,u.jsx)(t.strong,{children:`Fewer tokens spent on thinking.`}),` Across most benchmarks like GPQA-Diamond and MMLU-Pro, average output length drops by 10–14%, mostly from shorter chains of thought. In effect, part of the reasoning shifts from explicit output tokens into the implicit depth of the loop.`]}),`
`]}),`
`]}),`
`,(0,u.jsx)(t.h3,{children:`Inference Efficiency`}),`
`,(0,u.jsxs)(t.p,{children:[`GLM-5.4 reaches up to `,(0,u.jsx)(t.strong,{children:`200 tokens/s`}),` during off-peak hours and maintains `,(0,u.jsx)(t.strong,{children:`70–80 tokens/s`}),` at peak load. Achieving this throughput with a multi-pass Loop architecture required close co-design between the model and our inference infrastructure. Alongside the memory and retrieval savings from our KV cache and sparse index designs, we fused core kernels at the systems level to cut down intermediate memory reads and writes, eliminating the fragmented overhead amplified by looping.`]}),`
`,(0,u.jsx)(t.h2,{children:`Generalized Coding`}),`
`,(0,u.jsxs)(t.p,{children:[`Coding has become the foundation for extending model capabilities. Since going all-in on coding in early 2025, we have unlocked Agentic Engineering, Long-Horizon Tasks, and Cybersecurity. Now we are pushing toward `,(0,u.jsx)(t.strong,{children:`Generalized Coding`}),`. It has a higher ceiling and broader impact, and GLM-5.4 is just the starting point.`]}),`
`,(0,u.jsx)(t.p,{children:`Driven by improvements in both coding and vision, GLM-5.4 generalizes well beyond traditional software development. It can write code to generate and edit videos, build complete games, and handle 3D modeling and mechanical design:`}),`
`,(0,u.jsxs)(t.ul,{children:[`
`,(0,u.jsxs)(t.li,{children:[(0,u.jsx)(t.strong,{children:`Scaling Coding to Video:`}),` Producing `,(0,u.jsx)(t.em,{children:`"Hello World,"`}),` GLM-5.4’s self-narrated music video.`]}),`
`]}),`
`,(0,u.jsx)(`figure`,{className:`w-full h-fit`,style:{margin:0},children:(0,u.jsx)(`video`,{className:`w-[60rem] rounded-lg bg-cover bg-center bg-no-repeat`,src:`https://z-ai-bj.oss-cn-beijing.aliyuncs.com/prompts-rich-media-resources/5.4-blog/27570_1795400681.mp4`,controls:!0,loop:!0})}),`
`,(0,u.jsxs)(t.ul,{children:[`
`,(0,u.jsxs)(t.li,{children:[(0,u.jsx)(t.strong,{children:`Scaling Coding to Engineering:`}),` Building a 6-axis robotic arm through engineering-grade CAD modeling in FreeCAD.`]}),`
`]}),`
`,(0,u.jsx)(`figure`,{className:`w-full h-fit`,style:{margin:0},children:(0,u.jsx)(`video`,{className:`w-[60rem] rounded-lg bg-cover bg-center bg-no-repeat`,src:`https://z-ai-bj.oss-cn-beijing.aliyuncs.com/prompts-rich-media-resources/5.4-blog/1517_1795370530(原视频).mp4`,controls:!0,loop:!0})}),`
`,(0,u.jsxs)(t.ul,{children:[`
`,(0,u.jsxs)(t.li,{children:[(0,u.jsx)(t.strong,{children:`Scaling Coding to Games:`}),` Creating a complete game directly, covering character movement, physics, maps, combat systems, and art assets.`]}),`
`]}),`
`,(0,u.jsx)(`figure`,{className:`w-full h-fit`,style:{margin:0},children:(0,u.jsx)(`video`,{className:`w-[60rem] rounded-lg bg-cover bg-center bg-no-repeat`,src:`https://z-ai-bj.oss-cn-beijing.aliyuncs.com/prompts-rich-media-resources/5.4-blog/a2b99f0a783fafdbfdd9b6b19d104595_raw.mp4`,controls:!0,loop:!0})}),`
`,(0,u.jsxs)(t.ul,{children:[`
`,(0,u.jsxs)(t.li,{children:[(0,u.jsx)(t.strong,{children:`Scaling Coding to 3D:`}),` Generating an interactive 3D macro bird-watching experience from scratch using pure mathematical geometry and custom GLSL shaders.`]}),`
`]}),`
`,(0,u.jsx)(`figure`,{className:`w-full h-fit`,style:{margin:0},children:(0,u.jsx)(`video`,{className:`w-[60rem] rounded-lg bg-cover bg-center bg-no-repeat`,src:`https://z-ai-bj.oss-cn-beijing.aliyuncs.com/prompts-rich-media-resources/5.4-blog/331_1795422567_raw.mp4`,controls:!0,loop:!0})}),`
`,(0,u.jsx)(t.h2,{children:`Getting Started`}),`
`,(0,u.jsx)(t.p,{children:`Better performance, higher speed, and more generous usage quotas make GLM-5.4 practical for daily work. Try it here:`}),`
`,(0,u.jsxs)(t.ul,{children:[`
`,(0,u.jsxs)(t.li,{children:[`
`,(0,u.jsxs)(t.p,{children:[(0,u.jsx)(t.strong,{children:`GLM Coding Plan:`}),` `,(0,u.jsx)(t.a,{href:`https://z.ai/subscribe`,children:`https://z.ai/subscribe`})]}),`
`]}),`
`,(0,u.jsxs)(t.li,{children:[`
`,(0,u.jsxs)(t.p,{children:[(0,u.jsx)(t.strong,{children:`ZCode:`}),` `,(0,u.jsx)(t.a,{href:`https://zcode.z.ai/en`,children:`https://zcode.z.ai/en`})]}),`
`]}),`
`,(0,u.jsxs)(t.li,{children:[`
`,(0,u.jsxs)(t.p,{children:[(0,u.jsx)(t.strong,{children:`Z.ai Chat:`}),` `,(0,u.jsx)(t.a,{href:`https://chat.z.ai`,children:`https://chat.z.ai`})]}),`
`]}),`
`,(0,u.jsxs)(t.li,{children:[`
`,(0,u.jsxs)(t.p,{children:[(0,u.jsx)(t.strong,{children:`API (Coming Soon):`}),` `,(0,u.jsx)(t.a,{href:`https://z.ai/model-api`,children:`https://z.ai/model-api`})]}),`
`]}),`
`,(0,u.jsxs)(t.li,{children:[`
`,(0,u.jsxs)(t.p,{children:[(0,u.jsx)(t.strong,{children:`Open Weights:`}),` We plan to open-source the model weights responsibly after completing necessary safety hardening.`]}),`
`]}),`
`]}),`
`,(0,u.jsx)(t.h2,{children:`Looking Ahead`}),`
`,(0,u.jsx)(t.p,{children:`GLM-5.4 is our first step with looped architectures, and several questions remain open. We are exploring how to achieve adaptive compute so harder tokens dynamically get more iterations, and how the returns of looping behave as both loop count and model size keep growing.`}),`
`,(0,u.jsx)(t.p,{children:`We are not choosing between scaling depth and scaling model size; we are pursuing both. GLM-5.4 validates computational depth, and our next, significantly larger model will carry forward everything we learned here. It will be ready soon.`})]})}function f(e={}){let{wrapper:t}=e.components||{};return t?(0,u.jsx)(t,{...e,children:(0,u.jsx)(d,{...e})}):d(e)}(0,c.createRoot)(document.getElementById(`root`)).render((0,u.jsx)(l.StrictMode,{children:(0,u.jsx)(i,{date:`2026-11-23`,title:`GLM-5.4: Toward Generalized Coding with Our First Loop Transformer`,document:`https://docs.z.ai/guides/llm/glm-5.4`,chatZai:!0,tryZai:!1,callZai:!1,subscribeZai:!0,zcode:!0,children:(0,u.jsx)(t,{children:(0,u.jsx)(e,{en:f,components:a})})})}));