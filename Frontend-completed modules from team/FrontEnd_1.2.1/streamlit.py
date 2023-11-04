import streamlit as st
import requests
from bs4 import BeautifulSoup

#@st.cache_data
def editor_page():
    st.title("Editor-Page")
    st.markdown("""
        <style>
            .header {
                padding: 3rem 0;
                border-bottom: 1px solid #ccc;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .nav-links {
                display: flex;
                gap: 2rem;
            }
            #container {
                padding: 2rem;
            }
            #editor {
                margin-top: 2rem;
            }
        </style>
    """, unsafe_allow_html=True)

    st.write("""
        <div class="header">
            <div>
                <span>assets<span>
                <a href="#" class="link">upload</a>
            </div>
            <div class="nav-links">
                <a href="#" class="link">Home</a>
                <a href="#" class="link">Share</a>
                <a href="#" class="link">Submit</a>
                <a href="#" class="link">History</a>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.write("""
        <div id="container">
            <header>
                <span>File Outline<span>
            </header>
            <div id="editor">
                <textarea cols="75" rows="30" style="font-size: 20px;"></textarea>
            </div>
            <div>
                <iframe src="" width="100%" height="100%" allowfullscreen="True"></iframe>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Streamlit main content
    st.write("""
        <main class="container-fluid">
            <!-- Your Streamlit content goes here -->
        </main>
    """, unsafe_allow_html=True)

#@st.cache_data
def faq_data():
    st.markdown("""
<style>
    .faq-item {
        margin-bottom: 40px;
        margin-top: 40px;
    }
    .faq-body {
        display: none;
        margin-top: 30px;
    }
    .faq-wrapper {
        width: 75%;
        margin: 0 auto;
    }
    .faq-inner {
        padding: 30px;
        background: aliceblue;
    }
    .faq-plus {
        font-size: 1.4em;
        line-height: 1em;
        cursor: pointer;
    }
    hr {
        background-color: #9b9b9b;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="container mt-5 mb-5">
    <div class="row">
        <div class="faq-wrapper">
            <div class="header mb-5">
                <h1 class="text-center">Help & FAQs</h1>
            </div>
            <div class="faq-inner">
                <div class="faq-item">
                    <h3>
                        What is LaTeX ?
                        <span class="faq-plus">+</span>
                    </h3>
                    <div class="faq-body" id="faq1">
                        LATEX (pronounced “LAY-tek” or “LAH-tek”) is a tool for typesetting professional-looking documents. However, LaTeX’s mode of operation is quite different to many other document-production applications you may have used, such as Microsoft Word or LibreOffice Writer: those “WYSIWYG” tools provide users with an interactive page into which they type and edit their text and apply various forms of styling.
                    </div>
                </div>
                <hr>
                <div class="faq-item">
                    <h3>
                        Why learn LaTeX ?
                        <span class="faq-plus">+</span>
                    </h3>
                    <div class="faq-body" id="faq2">
                        Various arguments can be proposed for, or against, learning to use LATEX instead of other document-authoring applications; but, ultimately, it is a personal choice based on preferences, affinities, and documentation requirements.
                        <p><a href="https://www.overleaf.com/learn/latex/Learn_LaTeX_in_30_minutes#Why_learn_LaTeX.3F">Read More</a></p>
                    </div>
                </div>
                <hr>
                <div class="faq-item">
                    <h3>
                        The preamble of a document
                        <span class="faq-plus">+</span>
                    </h3>
                    <div class="faq-body" id="faq3">
                        The screengrab above shows Overleaf storing a LATEX document as a file called main.tex: the .tex file extension is, by convention, used when naming files containing your document’s LaTeX code.
                        <p><a href="https://www.overleaf.com/learn/latex/Learn_LaTeX_in_30_minutes#The_preamble_of_a_document">Read More</a></p>
                    </div>
                <hr>
                <div class="faq-item">
                    <h3>
                        Creating lists in LaTeX
                        <span class="faq-plus">+</span>
                    </h3>
                    <div class="faq-body" id="faq4">
                        You can create different types of list using environments, which are used to encapsulate the LaTeX code required to implement a specific typesetting feature. An environment starts with \\begin{environment-name} and ends with \\end{environment-name, where environment-name might be figure, tabular, or one of the list types: itemize for unordered lists or enumerate for ordered lists.
                        <p><a href="https://www.overleaf.com/learn/latex/Learn_LaTeX_in_30_minutes#Creating_lists_in_LaTeX">Read More</a></p>
                    </div>
                </div>
                <hr>
                <div class="faq-item">
                    <h3>
                        Finding and using LaTeX packages
                        <span class="faq-plus">+</span>
                    </h3>
                    <div class="faq-body" id="faq5">
                        LaTeX not only delivers significant typesetting capabilities but also provides a framework for extensibility through the use of add-on packages. Rather than attempting to provide commands and features that "try to do everything," LaTeX is designed to be extensible, allowing users to load external bodies of code (packages) that provide more specialist typesetting capabilities or extend LaTeX's built-in features, such as typesetting tables.
                        <p><a href="https://www.overleaf.com/learn/latex/Learn_LaTeX_in_30_minutes#Finding_and_using_LaTeX_packages">Read More</a></p>
                    </div>
                    <hr>
                    <div class="faq-item">
                        <h3>
                            Creating tables
                            <span class="faq-plus">+</span>
                        </h3>
                        <div class "faq-body" id="faq6">
                            The following examples show how to create tables in LaTeX, including the addition of lines (rules) and captions.
                            <p><a href="https://www.overleaf.com/learn/latex/Learn_LaTeX_in_30_minutes#Creating_tables">More</a></p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Streamlit interactive widgets to show/hide FAQ items
for i in range(1, 7):
    st.markdown(f"""
    <script>
        var faq{i}_visible = false;
    </script>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <style>
        #faq{i} {{
            cursor: pointer;
        }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <script>
        $("#faq{i}").on('click', function() {{
            faq{i}_visible = !faq{i}_visible;
            if (faq{i}_visible) {{
                $("#faq{i}").html('-');
                $("#faq{i} + .faq-body").show();
            }} else {{
                $("#faq{i}").html('+');
                $("#faq{i} + .faq-body").hide();
            }}
        }});
    </script>
    """, unsafe_allow_html=True)

#@st.cache_data
def for_groups():
    st.markdown("""
    <style>
        .b-example-divider {
            border: 1px solid #000;
            margin: 10px 0;
        }

        .text-center {
            text-align: center;
        }

        .container {
            padding: 10px;
        }

        .py-2 {
            padding-top: 20px;
            padding-bottom: 20px;
        }

        .py-5 {
            padding-top: 50px;
            padding-bottom: 50px;
        }

        .fw-bold {
            font-weight: bold;
        }

        .text-muted {
            color: #888;
        }

        .no-top-padding {
            padding-top: 0;
        }

        .btn-primary {
            background-color: #007bff;
            color: #fff;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            text-decoration: none;
        }

        .btn-primary:hover {
            background-color: #0056b3;
        }

        hr {
            border: none;
            border-top: 1px solid #000;
            margin: 20px 0;
        }

        .card {
            border: 1px solid #ccc;
            border-radius: 5px;
            padding: 20px;
            margin: 10px;
            background-color: #f8f8f8;
        }
    </style>
    """, unsafe_allow_html=True)

    st.write("""
    <div class="container">

    <div class="b-example-divider"></div>

    <div class="text-center container px-1 py-2">
        <h1 class="pb-2 border-bottom">For Groups </h1>
        <div class="row row-cols-1 row-cols-md-1 align-items-md-center py-5 ">
            <div class="d-flex flex-column text-center align-items-center gap-2">
                <h3 class="fw-bold ">Get TechDocs For Your Group</h3>
                <p class="text-muted align-content-center">TechDocs is an online collaborative writing and publishing tool
                    that makes the whole process of writing, editing and publishing scientific documents much quicker and
                    easier. TechDocs provides the convenience of an easy-to-use LaTeX editor with real-time collaboration and
                    the fully compiled output produced automatically in the background as you type.</p>
            </div>
        </div>
    </div>
    <div class="b-example-divider"></div>
    <div class="row row-cols-1 row-cols-md-1 align-items-md-center py-2 ">
        <section class=" no-top-padding">
            <div class="row section-row">
                <div class="col-xs-12 col-sm-12">
                    <div class="no-card text-center my-1">
                        <h2 id="plans">Know what you need? <div class = "my-2"></div><a href="{{url_for('plans')}}"
                                class="btn btn-primary btn-mt-3">Check Plans here</a> </h2>
                    </div>
                </div>
            </div>
        </section>
        <section class=" no-top-padding">
            <div class="row section-row">
                <div class="col-xs-12 col-sm-12">
                    <div class="no-card">
                        <hr />
                    </div>
                </div>
            </div>
        </section>
        <section class=" no-top-padding">
            <div class "row section-row">
                <div class="col-xs-12 col-sm-12">
                    <div class="no-card text-center">
                        <h2 id="why-move-to-a-group-license">Why Move To A Group License?</h2>
                    </div>
                </div>
            </div>
        </section>
        <section class=" no-top-padding">
            <div class="row section-row">
                <div class="col-xs-12 col-sm-12">
                    <div class="no-card text-center">
                        <p>Increase collaboration while reducing admin overheads with a group license for TechDocs, the
                            world's most popular collaborative LaTeX environment for labs, universities and businesses.</p>
                    </div>
                </div>
            </div>
        </section>
        <section class=" no-top-padding">
            <div class="row section-row">
                <div class="col-xs-12 col-sm-6">
                    <div class="card text-center">
                        <h2 id="cut-down-on-paperwork">Cut Down On Paperwork</h2>
                        <p>It's just one annual payment, and we'll work directly with your finance or purchasing department,
                            so you won't need to handle monthly TechDocs expenses.</p>
                    </div>
                </div>
                <div class="col-xs-12 col-sm-6">
                    <div class="card text-center">
                        <h2 id="simplify-latex-management">Simplify LaTeX Management</h2>
                        <p>Stop worrying about managing different LaTeX environments or tools and making sure they play well
                            together.</p>
                    </div>
                </div>
            </div>
        </section>
        <section class=" no-top-padding">
            <div class="row section-row">
                <div class="col-xs-12 col-sm-6">
                    <div class="card text-center">
                        <h2 id="promote-collaboration">Promote Collaboration</h2>
                        <p>TechDocs is built for collaboration. Multiple people working on the same project at the same time
                            is no problem with our easy-to-use track changes feature.</p>
                    </div>
                </div>
                <div class="col-xs-12 col-sm-6">
                    <div class="card text-center">
                        <h2 id="reduce-costs">Reduce Costs</h2>
                        <p>Give up to ten people in your group access to our full feature set.</p>
                    </div>
                </div>
            </div>
    </div>
    """, unsafe_allow_html=True)

#@st.cache_data
def for_publisher():
    st.markdown("""
<style>
    .container {
        padding: 20px;
    }

    .page-header h1 {
        font-size: 2em;
        font-weight: bold;
        margin-bottom: 20px;
    }

    .no-card {
        margin-bottom: 20px;
    }

    .nav-tabs {
        margin-top: 20px;
    }

    .nav-link {
        cursor: pointer;
    }

    .tab-content {
        margin-top: 20px;
    }

    .card {
        margin-top: 20px;
        padding: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.title("TechDocs for Publishers & Journals")

st.markdown("## Increase author satisfaction & reduce editorial headaches")

st.markdown("""
TechDocs is designed to provide authors and publishers with the tools to effectively
write, collaborate, submit, and manage an article through to publication—complementing existing project and
editorial management software.

Find out more about our different products and services below, or read through a selection of publisher
case studies on successful uses of TechDocs in different settings.

A comprehensive authoring collaboration tool, including publisher-specific template development or enhancement, options for “built in” automated pre-submission checks, author help desk and support, and publisher-specific simplified submission links into your submission system or to your submission web portal.
""")

section = st.selectbox("Select a section", ["TechDocs Services", "Benefits"])

if section == "TechDocs Services":
    st.markdown("""
    ### TechDocs Link
    A comprehensive authoring collaboration tool, including publisher-specific template development or enhancement, options for “built in” automated pre-submission checks, author help desk and support, and publisher-specific simplified submission links into your submission system or to your submission web portal.
    
    ### TechDocs LaTeX Validation Service
    The TechDocs LaTeX Validation Service allows third parties to use the TechDocs technology and servers to handle all of their LaTeX compilations automatically, via a managed API. This allows organizations to outsource the management and overhead of LaTeX technology upkeep, and better ensure that LaTeX documents compile correctly using the latest LaTeX versions and packages. By using TechDocs for compilation and validation, you’re providing your communities and teams with access to a state-of-the-art LaTeX installation – one which has compiled over 15 billion pages since 2013 – but without any of the management overhead.
    
    ### TechDocs Commons
    An TechDocs subscription service for organizations to provide TechDocs Professional accounts to their members and staff. This service provides streamlined, branded enrollment, a customized resource portal, user training and platform and template analytics/metrics.
    
    ### TechDocs Group Subscriptions
    A set number of TechDocs Collaborator or Professional accounts for members and staff. Group subscriptions include a team management dashboard to add and remove team members, Centralized billing and admin, and an option to reassign licenses as needed.
    """)

if section == "Benefits":
    st.markdown("""
    TechDocs offers publishers an innovative, simple-to-implement authoring and submission solution, serving as a useful author resource and significantly enhancing author satisfaction. TechDocs can also alleviate the pressures that LaTeX and templated submissions might have on your editing and production personnel.

    **Features & Benefits:**
    - **Benefit from a fast and simple LaTeX submission process:** ensure that LaTeX submissions arrive in the correct format with all publisher requirements followed and confirmed, all documentation present and error-free compilation.
    - **Provide authors with a simplified submission process:** from their paper in TechDocs to your submission system or submission web portal – easing and streamlining the submission process.
    - **Help authors follow the correct format and guidelines:** by providing your custom LaTeX templates and through the automated TechDocs pre-submission check system.
    - **Support author collaboration in your community:** by providing an innovative writing tool that simplifies their writing process, expands and facilitates their cloud collaboration ability, and streamlines their workflow and publisher submission process.
    - **Ensure the authoring, reviewing, and editing experience is smooth, simple, and painless:** by having a trusted tool that will support your aims and goals.
    - **Outsource LaTeX support:** by having the TechDocs ‘TeX’perts handle all LaTeX and technical questions directly.
    - **LaTeX, evolved** - provide your authors and communities with access to a state-of-the-art LaTeX installation, but without any of the management overhead.
    """)

#@st.cache_data
def for_teaching():
    # Header
    st.title("For Teaching")
    # Introduction
    st.markdown(
        "TechDocs is utilized at universities all around the world to teach mathematics, physics, and other subjects. "
        "Instructors use TechDocs in class for interactive demos and offer students with templated assignments that "
        "they can access and edit securely online—nothing has to be installed to get started."
    )
    # Tab navigation
    tabs = ["Getting Started", "Creating Class Materials"]
    selected_tab = st.radio("Choose a Tab", tabs, key="unique_key_for_radio_widget")

    if selected_tab == "Getting Started":
        st.subheader("Getting Started")
        st.markdown(
            "To begin using TechDocs, just sign up for a free account and invite your students to do the same.\n\n"
            "Your students will be able to take advantage of the convenience of an easy-to-use LaTeX editor with "
            "real-time collaboration after they've signed up, with nothing to download or install - they can get "
            "started right away."
        )

    elif selected_tab == "Creating Class Materials":
        st.subheader("Creating Class Materials")
        st.markdown(
            "There are three simple methods for making your templates and other class resources available to students "
            "who use TechDocs for their assignments:\n\n"
            "- Using our link sharing function is the simplest method to share an assignment with your students. You may "
            "provide your assignment as a read-only project, which they can then duplicate and complete before submitting.\n\n"
            "- You may post your templates and examples in the TechDocs gallery so that your students can utilise them right "
            "away. This article will teach you how to publish templates on TechDocs.\n\n"
            "- If you want to host your own LaTeX templates, you may use our API to generate simple links to open them in "
            "TechDocs. It's as simple as clicking Open this homework assignment to see for yourself. Every student who "
            "clicks the link will generate their own personal copy to fill out and submit."
        )

    # For Universities section
    st.title("For Universities")

    st.markdown(
        "TechDocs is an online collaborative writing and publishing tool that makes the whole process of writing, "
        "editing and publishing scientific documents much quicker and easier. TechDocs provides the convenience of "
        "an easy-to-use LaTeX editor with real-time collaboration and the fully compiled output produced automatically "
        "in the background as you type."
    )

    # TechDocs Commons section
    st.markdown("### TechDocs Commons includes:")
    st.markdown(
        "- **TechDocs Professional accounts** – for students, faculty, and staff.\n"
        "- **Hassle-free license management** – users simply register with their institutional email address on TechDocs "
        "(or add it to their existing TechDocs account) to join your TechDocs Commons license and receive their upgrade "
        "automatically.\n"
        "- **An TechDocs resource portal** – featuring templates, FAQs, and Help resources, and a quick way for new users "
        "to sign up.\n"
        "- **Support** – we’ll help you get everything set up and then we’re here to answer questions from students, "
        "faculty, and staff about the platform, templates, or LaTeX itself!\n"
        "- **Training videos and webinars** – to help ensure your users and admin staff are ready to use the TechDocs platform.\n"
        "- **Metrics and analytics** – we provide an administrative dashboard with metrics and analytics on platform use, "
        "users, projects, and submissions."
    )

    # Contact Us section
    st.markdown("### Contact Us for our Service kit to help gather support internally")
    st.markdown(
        "If you'd like to find out more about how TechDocs can support your students and researchers, please get in touch, "
        "we'd love to hear from you. Includes instructions and a letter for your favorite librarian, head of department, "
        "or other decision maker."
    )

#@st.cache_data
def for_writing():
    # Header
    st.title("For Authors")

    # Introduction
    st.markdown(
        "The TechDocs collaborative writing tool makes it much easier and quicker to write, edit, and publish scientific "
        "documents online. As you type, TechDocs produces fully compiled output automatically in the background and an "
        "easy-to-use LaTeX editor with real-time collaboration TechDocs is an online collaborative writing and publishing "
        "tool that makes the whole process of writing, editing and publishing scientific documents much quicker and easier. "
        "TechDocs provides the convenience of an easy-to-use LaTeX editor with real-time collaboration and the fully compiled "
        "output produced automatically in the background as you type."
    )

    # Sign Up button
    st.button("Sign Up for Free", key="10")
    # Features section
    st.markdown("## Features")
    features = [
        {
            "title": "All you need is a web browser",
            "description": "Using our real-time preview, you will see how your final project looks as you type. There is no "
                        "software to install, so you can start writing and collaborating immediately. "
                        "Prefer to work offline? No problem, you can stay in sync with Github."
        },
        {
            "title": "Always have the latest version",
            "description": "When you use TechDocs, you can access your documents from any device at any time, so you never "
                        "have to worry about leaving a crucial document at home while you're away. Working together with "
                        "others? Everyone always has the most recent version because of TechDocs' transparent "
                        "synchronization of updates across all authors."
        },
        {
            "title": "Effortless Sharing",
            "description": "TechDocs gives you two simple ways to share your work with collaborators: via private invitation or by "
                        "providing a link. By default, every document you produce there is private. You can distribute your "
                        "creations by using secure connections with link sharing. Simply enable link sharing, send your "
                        "co-authors the link, and they may read, comment on, and edit. You might also just disable the link "
                        "to make your project private once more. With private invitations, you can give access to your projects "
                        "to a limited number of named collaborators; the number of named collaborators you can invite for each "
                        "project depends on your plan. View the plans and costs at TechDocs."
        },
        {
            "title": "Automatic real-time preview",
            "description": "Your project is securely compiled by TechDocs so that you can immediately view the finished PDF. "
                        "You can turn it on or off as you like. It's helpful for learning and preventing the accumulation of "
                        "errors in your project."
        },
        {
            "title": "Real-time track changes and commenting",
            "description": "You can discuss your work with real-time commenting and integrated chat without having to switch to "
                        "email, printed versions, or any other tool. Within TechDocs, you can leave comments, provide quick "
                        "feedback, and resolve issues. You can also keep track of every change made to your project and who made "
                        "it on an upgraded plan. You can easily see what changes your co-authors or reviewers have made and how "
                        "they affect the document. Accept or reject individual changes with the click of a button, then move on "
                        "to the next change that requires your attention, all within the editor."
        },
        {
            "title": "Complementary Rich Text and LaTeX modes",
            "description": "Do you want to see less code when you're writing? Or are you dealing with colleagues who are more "
                        "comfortable with WYSIWYG editors like MS Word? If this is the case, just switch to the rich text mode "
                        "of TechDocs, which produces headlines, pictures, formatting, and equations right in the editor. Of course, "
                        "if you prefer to edit directly in LaTeX, you can switch back to that at any time."
        },
        {
            "title": "Quickly find LaTeX errors",
            "description": "TechDocs highlights problems and warnings as you go, allowing you to notice them early and eliminating "
                        "the need to search for them in the LaTeX log."
        }
    ]

    for feature in features:
        st.markdown(f"### {feature['title']}")
        st.write(feature['description'])

#@st.cache_data
def premium_features():
    st.write(
    "Contents",
    "<ul>"
    "<li><a href='#Invite_more_collaborators'>Invite more collaborators</a></li>"
    "<li><a href='#Increased_compile_timeout'>Increased compile timeout</a></li>"
    "<li><a href='#Real-time_track_changes'>Real-time track changes</a></li>"
    "<li><a href='#Full_document_history_and_versioning'>Full document history and versioning</a></li>"
    "<li><a href='#Advanced_reference_search'>Advanced reference search</a></li>"
    "<li><a href='#Reference_manager_synchronization'>Reference manager synchronization</a></li>"
    "<li><a href='#GitHub_synchronization'>GitHub synchronization</a></li>"
    "<li><a href='#Symbol_Palette'>Symbol Palette</a></li>"
    "<li><a href='#Priority_Support'>Priority Support</a></li>"
    "<li><a href='#Further_information'>Further information</a>"
    "<ul>"
    "<li><a href='#Account_and_project_level_features'>Account and project level features</a></li>"
    "<li><a href='#More_help'>More help</a></li>"
    "</ul>"
    "</li>"
    "</ul>",
    unsafe_allow_html=True,
)

st.header("Invite more collaborators")
st.write(
    "You can invite named collaborators to your project via the ‘share’ menu in your project (with read-only or edit access). "
    "Simply add their email address and an email invitation will be sent to them. You can remove these named collaborators at any time via the same ‘share’ menu. The number of named collaborators you can invite depends on your plan."
)
st.table(
    [
        ["", "Free", "Personal", "Standard", "Professional"],
        ["Number of collaborators", 1, 1, 10, "unlimited"],
    ]
)
st.write("[Read More](#)")

st.header("Increased compile timeout")
st.write("You have more time for compilation (to generate a PDF of your document) before receiving a timeout error message.")
st.write("[Read More](#)")

st.header("Real-time track changes")
st.write(
    "The track changes mode lets you see exactly what has been changed by your collaborators, "
    "and allows you to accept or reject each individual change. The track changes feature is not available on projects owned by users of the Free or Personal plans."
)
st.write("[Read More](#)")

st.header("Full document history and versioning")
st.write(
    "View the entire history of your project with the ability to revert to previous versions of your document from your project history (versus only 24 hours of history availability on a free TechDocs account). No more fear of losing work or making changes you can’t undo."
)
st.write("[Read More](#) [Read More](#)")

st.header("Advanced reference search")
st.write(
    "You can search by citation key, and our premium feature allows the added ability to search by author, title, year, or journal."
)
st.write("[Read More](#)")

st.header("Reference manager synchronization")
st.write(
    "You can link your Mendeley and Zotero accounts to your TechDocs account, allowing you to import your reference library and keep your TechDocs document in sync with the references stored in Mendeley / Zotero."
)
st.write("[Read More](#)")

st.header("GitHub synchronization")
st.write(
    "You can configure your TechDocs project to synchronize directly with a repository on GitHub, or you can use raw git access. This allows you to work offline and synchronize your files whenever you come back online. You can also use our TechDocs Git Bridge integration, which lets you git clone, push, and pull changes between the online TechDocs editor and your local offline git repository."
)
st.write("[Read More](#)")

st.header("Symbol Palette")
st.write("The Symbol Palette is a convenient tool to quickly insert math symbols into your document. It’s an account level feature, which is explained in more detail below.")
st.write("[Read More](#)")

st.header("Priority Support")
st.write(
    "Our helpful Support team will prioritize and escalate your support requests where necessary. Please note that we do not provide additional debugging support for users on a premium plan."
)
st.write("[Read More](#)")

st.header("Further information")

st.subheader("Account and project level features")
st.write(
    "Please note that certain premium features apply at the project level, like track-changes, compile time, and access to full history, and are based on the project owner's subscription. So, when invited to collaborate on a project owned by someone with a subscription, users on the free plan can use those features within that project."
)
st.write(
    "In other words, if you yourself have an upgraded account, your fellow collaborators do not need to pay for a subscription in order to use track-changes or access the full history within projects that you share with them."
)
st.write(
    "Other premium features apply at the account level, and are controlled by you, the subscription holder. These are the features which include linking to external services, like Dropbox, GitHub, Git, Mendeley, and Zotero. The majority of these do also confer benefits to those you work with, as described below:"
)
st.write("GitHub: A user with a premium subscription can link any project they own to a GitHub repo. Once the project is linked, all users in the project can click the button to sync it. So this can be thought of as a 'per project' feature.")
st.write(
    "Git: If the project is owned by a user with a premium subscription, all members of the project can git clone/push/pull to it. If a user has a premium subscription, they can git clone/push/pull to all projects they have access to. This is like a superset of GitHub and Dropbox permission model - it's personal, and per project."
)
st.write("Symbol Palette: A user with a premium subscription always has access to this feature regardless of which project they are working on.")
st.write("[Read More](#)")
st.subheader("More help")
st.write("For further reading on how to get the most out of TechDocs Help page. This includes a wide range of platform guidance, LaTeX tutorials & technical articles.")

#@st.cache_data
def forgot_password():

    # CSS link
    st.markdown('<link rel="stylesheet" type="text/css" href="static/css/forgotpassword.css">', unsafe_allow_html=True)

    # JavaScript link
    st.markdown('<script src="js/forgotpassword.js"></script>', unsafe_allow_html=True)

    # Header
    st.title("Forgot Password")

    # Form
    # Initialize a counter variable
    #Inside your Streamlit app, when creating widgets:
    st.write("Enter your email address to reset your password.")
    email = st.text_input("Email address", key="1")
    if st.button("Reset your password"):
        # Password reset logic here
        st.success("Password reset instructions sent to your email.")

#@st.cache_data
def reset_password():
    # CSS link
    st.markdown('<link rel="stylesheet" type="text/css" href="static/css/resetpassword.css">', unsafe_allow_html=True)

    # JavaScript link
    st.markdown('<script src="js/resetpassword.js"></script>', unsafe_allow_html=True)

    # Header
    st.title("Reset Password")

    # Loading button
    st.write("Loading...")
    with st.spinner():
        # Simulate a loading process here
        st.markdown("Loading complete")

    # Display error message
    valid_token_error_message = st.empty()

    # Form
    st.write("Please enter your new password to reset your account.")
    new_password = st.text_input("New Password", type="password", key="password1")
    confirm_password = st.text_input("Confirm Password", type="password", key="password 2")

    if st.button("Change", key="3"):
        # Password change logic here
        if new_password == confirm_password:
            # Passwords match, proceed with password change
            st.success("Password has been successfully changed.")
        else:
            valid_token_error_message.error("Password and confirm password do not match. Please try again.")
        return st.button("Click me!", key="4")

def home_page():
    #     # Page layout
    # st.set_page_config(
    #     page_title="TechDocs",
    #     page_icon="📄",
    #     layout="centered",
    # )

    # Link to CSS file
    st.markdown('<link rel="stylesheet" type="text/css" href="./style.css">', unsafe_allow_html=True)

    # Content
    st.write("")
    # st.image("path/to/your/images/h2.png", use_column_width=True)

    st.write(
        """
        # TechDocs

        It is a dockerized, mobile-ready, offline-storage compatible, JS-powered LaTeX editor.

        [Register](registration)
        """
    )

    # st.image("", use_column_width=True)  # Add your images here
    # st.image("", use_column_width=True)  # Add your images here

def home_page1():
    # Add custom CSS
    st.markdown(
        '<link rel="stylesheet" type="text/css" href="css/styleH.css">',
        unsafe_allow_html=True,
    )

    # Navigation bar
    st.markdown('<div class="navbar background">', unsafe_allow_html=True)
    st.markdown(
        """
        <ul class="nav-list another">
            <div class="logo"><img src="techdocs-minimal.png" alt="logo"></div>
            <li><a href="Home">Home</a></li>
            <li><a href="Features">Features</a></li>
            <li><a href="Pricing">Pricing</a></li>
            <li><a href="Help">Help</a></li>
        </ul>
        <div class="rightnav">
            <input type="text" name="REGISTER" id="REGISTER">
            <input type="password" name="User pass" id="txtpwd">
            <button class="btn btn-sm" style="background-color: rgb(174, 220, 241)">REGISTER</button>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # Main content
    st.markdown('<section class="background fisrtsection">', unsafe_allow_html=True)
    st.markdown('<div class="box-main">', unsafe_allow_html=True)
    st.markdown('<div class="firsthalf">', unsafe_allow_html=True)
    st.markdown("## THE EVOLUTION OF DOCUMENTATION IS HERE", unsafe_allow_html=True)
    st.markdown("It is a dockerized, mobile-ready, offline-storage compatible, JS-powered LaTeX editor", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="buttons">
            <button class="btn btncolor">Login</button>
            <button class="btn btncolor">Sign Up</button>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="secondhalf">', unsafe_allow_html=True)
    # st.image("img/techdoclogo.png", use_column_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</section>", unsafe_allow_html=True)

    st.markdown('<section class="secright"></section>', unsafe_allow_html=True)
    st.markdown("## Ease Of Use", unsafe_allow_html=True)
    st.markdown(
        """
        There’s nothing complicated or difficult for you to install, and you can start using LaTeX right now, even if you’ve never seen it before. TECHDOC comes with a complete, ready to go LaTeX environment which runs on our servers.

        With TECHDOC, you get the same LaTeX set-up wherever you go. By working with your colleagues and students on TECHDOC, you know that you’re not going to hit any version inconsistencies or package conflicts.

        We support almost all LaTeX features, including inserting images, bibliographies, equations, and much more! Read about all the exciting things you can do with TECHDOC in our LaTeX guides.
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="thumbnail"></div>', unsafe_allow_html=True)
    # st.image("", use_column_width=True)  # Add your image source

def latex_editor():
    st.subheader("LATEX EDITOR")
    doc_id = "new-document"  # You can replace this with the actual document ID
    template = st.selectbox("Select a section", ["TechDocs Services", "Benefits"], key="unique_key_for_selectbox")

    if template == "Resume":
        # Insert your resume content here
        doc_text = r"""\documentclass{article}
    \usepackage{comment, multicol}
    \usepackage{hyperref}
    \usepackage{calc,pict2e,picture}
    \usepackage{textgreek,textcomp,gensymb,stix}
    \setcounter{secnumdepth}{2}
    \title{Person Fullname}
    \author{}
    \date{email@id.domain | 810xxxxxx3}
    \begin{document}
    \maketitle
    This is a small intro about yourself, while at the same time being a gentle introduction to \LaTeX.
    In the appendix, the API as well as the format of custom macro definitions in JavaScript will be explained.
    \section{Experiences}
    \begin{itemize}
        \item Project one description followed by skills used
        \item Project Two description followed by skills used
        \item Project Three description followed by skills used
    \end{itemize}
    \bigskip
    \section{Education}
    \bigskip
    \section{Personal Details}
    \end{document}
    """

    else:
        doc_text = ""

    doc_text = st.text_area("Edit the document", doc_text)

    # Display the HTML preview
    if st.button("Generate HTML Preview"):
        response = requests.post("http://techdocs-api.previewbox.in/api/generate", json={"doc_text": doc_text})
        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, "html.parser")
            st.components.v1.html(soup.prettify(), width=800, height=400)
        else:
            st.error("Error generating HTML preview")

    # Saving the document
    if st.button("Save Document"):
        # Insert code to save the document
        st.success("Document saved successfully")

def latex_history():
    st.title("History")

    with st.container():
        with st.expander("60 mins ago"):
            st.write("John edited an item.")
            st.write("[Filename.ext](#)")

        with st.expander("80 mins ago"):
            st.write("Smith edited an item.")
            st.write("[Filename.ext](#)")

def login():
    st.subheader("Login")
    st.markdown(
    """
    <style>
      #login-container {
        max-width: 380px;
        margin: auto;
        text-align: center;
      }
      a {
        text-decoration: none;
      }
    </style>
    """,
    unsafe_allow_html=True,
    )

# Main content
    st.markdown('<div id="login-container" class="mt-3">', unsafe_allow_html=True)
    st.markdown("## User Login", unsafe_allow_html=True)
    st.markdown("")

    # Create a password input
    password = st.text_input("Password", type="password", key="password")

    # Check if the password input is not empty
    if password:
        st.write(f"You entered the following password: {password}")

    st.markdown("")
    st.markdown('<a href="URL_TO_YOUR_FORGOT_PASSWORD_PAGE">Forgot Password</a>', unsafe_allow_html=True)
    st.markdown("")

    # Create a "Login" button
    if st.button("Login"):
        st.write("Login button clicked")

    st.markdown('<div class=" mt-2">', unsafe_allow_html=True)
    st.markdown('<div class="d-flex mt-3 mb-3">', unsafe_allow_html=True)
    st.markdown('<div class="flex-fill">', unsafe_allow_html=True)
    st.markdown("<hr />", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown('<div class="flex-fill">OR</div>', unsafe_allow_html=True)
    st.markdown('<div class="flex-fill">', unsafe_allow_html=True)
    st.markdown("<hr />", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown('<span id="google-login-errorMessage" class="errorMessage"></span>', unsafe_allow_html=True)
    st.markdown('<div id="googleLogin"></div>', unsafe_allow_html=True)
    st.markdown("")

    # Create a link to the registration page
    st.markdown("Not a User? [Register](URL_TO_YOUR_REGISTRATION_PAGE)", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def payment_summary():
    st.title("Payment Page")

# Page CSS
    st.markdown("""
    <style>
        #container {
            text-align: center;
            max-width: 1200px;
            margin: auto;
        }
        .header {
            border-top: 1px solid #000;
        }
        .col-25 {
            width: 25%;
        }
        .list {
            list-style: square;
        }
    </style>
    """, unsafe_allow_html=True)

    # Link to CSS file
    st.markdown('<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/payment.css\') }}">', unsafe_allow_html=True)

    # Main content container
    st.markdown("<div id='container'>", unsafe_allow_html=True)

    # Summary
    st.markdown("<div class='col-25'>", unsafe_allow_html=True)
    st.markdown("<h2>Summary</h2>", unsafe_allow_html=True)
    st.markdown("<div class='list'>", unsafe_allow_html=True)
    st.markdown("<h4 id='PlanName'>Premium Monthly Subscription</h4>", unsafe_allow_html=True)
    st.markdown("<ul>", unsafe_allow_html=True)
    st.markdown("<li class='list'>Plagiarism check</li>", unsafe_allow_html=True)
    st.markdown("<li class='list'>Sharing with multiple people (to edit)</li>", unsafe_allow_html=True)
    st.markdown("<li class='list'>Extra storage - upgrade</li>", unsafe_allow_html=True)
    st.markdown("<li class='list'>Product Analytics - based on user behaviour</li>", unsafe_allow_html=True)
    st.markdown("<li class='list'>Word meanings/suggestions</li>", unsafe_allow_html=True)
    st.markdown("<li class='list'>Web scraping</li>", unsafe_allow_html=True)
    st.markdown("<li class='list'>Image to Word converter</li>", unsafe_allow_html=True)
    st.markdown("<li class='list'>Watermarking</li>", unsafe_allow_html=True)
    st.markdown("</ul>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<hr />", unsafe_allow_html=True)
    st.markdown("<h2>Payment Summary</h2>", unsafe_allow_html=True)
    st.markdown("<pre><span id='PlanName2'>Premium Monthly Subscription</span>       <span id='Price'>₹199</span></pre>", unsafe_allow_html=True)
    st.markdown("<pre>Total Payable                      <span id='Price2'>₹199</span>(Incl. all taxes)</pre>", unsafe_allow_html=True)
    st.markdown("<br />", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Payment form
    st.markdown("<div class='col-75'>", unsafe_allow_html=True)
    st.markdown("<form action='/action_page.php'>", unsafe_allow_html=True)
    st.markdown("<div class='row'>", unsafe_allow_html=True)
    st.markdown("<div class='col-50'>", unsafe_allow_html=True)
    st.markdown("<h3>Payment</h3>", unsafe_allow_html=True)
    st.text_input("Full Name", key="fname", value="XYZ")
    st.text_input("Email", key="email", value="XYZ@example.com")
    st.text_input("Address", key="adr", value="XYZ Street")
    st.text_input("City", key="city", value="HYDERABAD")
    st.text_input("State", key="state", value="TS")
    st.text_input("Zip", key="zip", value="500036")
    st.selectbox("Country", ["Select a country ... ", "Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cameroon", "Cape Verde", "Central African Republic", "Chad", "Comoros", "Congo - Brazzaville", "Congo - Kinshasa", "Côte d’Ivoire", "Djibouti", "Egypt", "Equatorial Guinea", "Eritrea", "Ethiopia", "Gabon", "Gambia", "Ghana", "Guinea", "Guinea-Bissau", "Kenya", "Lesotho", "Liberia", "Libya", "Madagascar", "Malawi", "Mali", "Mauritania", "Mauritius", "Mayotte", "Morocco", "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda", "Réunion", "Saint Helena", "Senegal", "Seychelles", "Sierra Leone", "Somalia", "South Africa", "Sudan", "Swaziland", "São Tomé and Príncipe", "Tanzania", "Togo", "Tunisia", "Uganda", "Western Sahara", "Zambia", "Zimbabwe"])
    st.markdown("<div class='col-50'>", unsafe_allow_html=True)
    st.markdown("<input type='submit' value='Continue to checkout' class='btn'>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</form>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # JavaScript to update prices
    st.markdown("<script>", unsafe_allow_html=True)
    st.markdown("Price: ₹199")
    st.markdown("Plan Name: Premium Monthly Subscription")
    st.markdown("Price2: ₹199")
    st.markdown("Plan Name2: Premium Monthly Subscription")
    st.markdown("</script>", unsafe_allow_html=True)

def pricing():
        # Define CSS for the entire application
    st.markdown(
        """
        <style>
        .container {
            margin-top: 5rem;
            text-align: center;
        }

        .section-intro {
            text-align: center;
        }

        .toggle-switch-container {
            text-align: center;
        }

        .plan-card {
            text-align: center;
            padding: 1rem;
            border: 1px solid #ccc;
            border-radius: 5px;
        }

        .card-pricing_header {
            font-size: 24px;
            font-weight: bold;
        }

        .card-pricing_price {
            font-size: 36px;
            font-weight: bold;
        }

        .card-pricing_button-1 .button-01 {
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            cursor: pointer;
        }

        .card-pricing_button .button {
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            cursor: pointer;
        }

        .disabled {
            background-color: #ccc;
            cursor: not-allowed;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.title("Pricing & Subscriptions")
    st.header("Choose your desired plan")

    # Add a toggle switch for Monthly/Yearly
    if st.checkbox("Yearly"):
        st.write("You've selected Yearly plan.")
    else:
        st.write("You've selected Monthly plan.")

    st.markdown("## Pricing Cards")

    st.subheader("Standard")
    st.markdown("Free Plan")
    st.markdown("₹0")

    # Button for BasicPlan
    if st.button("Get Started"):
        st.write("Redirecting to BasicPlan...")  # You can add a redirection logic here

    st.markdown("### Standard Features:")
    st.markdown("&#9758; Convert to PDF")
    st.markdown("&#9758; Spell Check")
    st.markdown("&#9758; Grammar check")
    st.markdown("&#9758; Search completion")

    st.subheader("Premium")
    st.markdown("Get More Features")
    st.markdown("₹199 / mo")

    # Button for PremiumPlan (Currently disabled)
    st.markdown('<button class="button disabled">Coming Soon</button>', unsafe_allow_html=True)

    st.markdown("### Premium Features:")
    st.markdown("&#8592; Everything in Standard Plan +")
    st.markdown("&#9758; Plagiarism check")
    st.markdown("&#9758; Sharing with multiple people")
    st.markdown("&#9758; Extra storage - upgrade")
    st.markdown("&#9758; Product Analytics - based on user behaviour")
    st.markdown("&#9758; Word meanings/suggestions")

def user_plan():
    st.markdown(
    """
    <style>
    .container {
        margin-top: 5rem;
        text-align: center;
    }

    .section-intro {
        text-align: center;
    }

    .toggle-switch-container {
        text-align: center;
    }

    .plan-card {
        text-align: center;
        padding: 1rem;
        border: 1px solid #ccc;
        border-radius: 5px;
    }

    .card-pricing_header {
        font-size: 24px;
        font-weight: bold;
    }

    .card-pricing_price {
        font-size: 36px;
        font-weight: bold;
    }

    .card-pricing_button-1 .button-01 {
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        cursor: pointer;
    }

    .card-pricing_button .button {
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        cursor: pointer;
    }

    .disabled {
        background-color: #ccc;
        cursor: not-allowed;
    }
    </style>
    """, unsafe_allow_html=True)

# Page content
    st.title("Pricing & Subscriptions")
    st.header("Upgrade your plan")

    # Toggle switch
    plan_switch = st.checkbox("Yearly / Monthly")
    if plan_switch:
        st.write("You selected Yearly plan.")
    else:
        st.write("You selected Monthly plan.")

    # Pricing cards
    st.subheader("Pricing Cards")

    st.write("## Standard Plan")
    st.write("Free Plan")
    st.write("Price: ₹0")
    st.button("Current Plan")

    st.write("Features:")
    st.write("- Convert to PDF")
    st.write("- Spell Check")
    st.write("- Grammar check")
    st.write("- Search completion")

    st.write("## Premium Plan")
    st.write("Get More Features")
    st.write("Price: ₹199 / mo")
    purchase_button = st.button("Purchase Now")
    if purchase_button:
        st.write("Redirect to payment summary page.")

    st.write("Features:")
    st.write("Everything in Standard Plan +")
    st.write("- Plagiarism check")
    st.write("- Sharing with multiple people")
    st.write("- Extra storage - upgrade")
    st.write("- Product Analytics - based on user behavior")
    st.write("- Word meanings/suggestions")

    # Compare button
    st.subheader("Compare Plans")
    compare_button = st.button("Show Compare Plans")

    if compare_button:
        # Render comparison table here
        st.subheader("Comparison Table")
        st.write("Plan Comparison goes here.")

    # JavaScript
    st.write('<script src="js/user-plan.js"></script>', unsafe_allow_html=True)

def user_profile():
    st.markdown(
    """
    <style>
        .dropdown-menu {
            width: 100px;
        }
    </style>
    """,
    unsafe_allow_html=True,
    )

    st.title("User Account Settings")

    # Define sections using beta_expander
    with st.expander("Update Profile Info"):
        col1, col2 = st.columns(2)
        col1.write("Signed up on")
        col1.write("Last Active")
        
        first_name = col2.text_input("First Name")
        last_name = col2.text_input("Last Name")
        address = col2.text_input("Street Address")
        country = col2.selectbox("Country", ["Country 1", "Country 2", "Country 3"])
        state = col2.selectbox("State", ["State 1", "State 2", "State 3"])
        occupation = col2.text_input("Occupation")
        purpose = col2.selectbox("Purpose of use", ["Research", "Commercial", "Student"])

        if st.button("Update"):
            # Handle the update action here
            st.write(f"Updating Profile Info: First Name: {first_name}, Last Name: {last_name}, Address: {address}, Country: {country}, State: {state}, Occupation: {occupation}, Purpose: {purpose}")

    with st.expander("Change Password"):
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password", key="new_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")

        if st.button("Change Password", key="change_password"):
            # Handle the change password action here
            st.write(f"Changing Password: Current Password: {current_password}, New Password: {new_password}, Confirm Password: {confirm_password}")

    with st.expander("Delete Account"):
        st.write("This will delete your account & all associated files")
        delete_password = st.text_input("Password", type="password", key="delete_password")
        confirm_delete = st.checkbox("Confirm that you understand the consequences", key="confirm_delete")

        if st.button("Delete Account", key="delete_account"):
            # Handle the delete account action here
            st.write(f"Deleting Account: Password: {delete_password}, Confirm Delete: {confirm_delete}")

    with st.expander("Link to Cloud Store"):
        st.write("Not in scope currently")

def register():
    st.subheader("Marketing Page")

# Add content to your marketing page
    st.header("Welcome to our Marketing Page")
    st.write("This is your marketing content.")

def dashboard():
    st.title("Dashboard")

    st.write("Welcome to your dashboard. Here you can manage your documents.")

    # PAGE HEADER AND SEARCH
    st.subheader("Page Header and Search")

    # New Document Button
    if st.button("New Document"):
        option = st.selectbox("Select a template:", ["Resume Template", "Blank Template"])
        if option == "Resume Template":
            st.write("Creating a new resume template document.")
        elif option == "Blank Template":
            st.write("Creating a new blank document.")

    # Share, Archive, and Move to Trash Buttons
    st.write("Manage your documents:")
    if st.button("Share", key="share-doc"):
        st.write("Sharing document.")
    if st.button("Archive", key="archive-doc"):
        st.write("Archiving document.")
    if st.button("Move to Trash", key="trash-doc"):
        st.write("Moving document to trash.")

    # Search Input
    search_query = st.text_input("Search files", key="searchfile")
    st.write(f"Searching for files with query: {search_query}")

    # USER TABLES
    st.subheader("User Tables")

    # Display the first table
    st.write("Table 1: User Table 1")

    # Display the second table
    st.write("Table 2: User Table 2")

    # Include JavaScript for interactive features (not implemented in this example)

    # END OF PAGE HEADER AND SEARCH
    # END OF USER TABLES
    st.subheader("Button Menu (Marketing Page)")

# Create buttons for marketing page (Continuation)
    marketing_button_1 = st.button("Marketing Button 1")
    marketing_button_2 = st.button("Marketing Button 2")

    if marketing_button_1:
        st.write("Marketing Button 1 clicked.")
    elif marketing_button_2:
        st.write("Marketing Button 2 clicked.")

def user_registration():
    st.write("# User Registration")

# User Registration Form
    firstname = st.text_input("First Name", key="firstname")
    lastname = st.text_input("Last Name", key="lastname")
    email = st.text_input("Email Address", key="email_1")
    password = st.text_input("Password", type="password", key="password_input")
    password_confirm = st.text_input("Confirm Password", type="password", key="password_confirm")

    # Registration Error and Info Messages
    register_error_message = st.empty()
    register_info_message = st.empty()

    # Register Button
    if st.button("Register", key="register"):
        if not firstname or not lastname or not email or not password or not password_confirm:
            register_error_message.error("All fields are required.")
        elif password != password_confirm:
            register_error_message.error("Passwords do not match.")
        else:
            # Handle the registration logic here
            register_info_message.success("Registration successful. You can now log in.")

    # Link to Login Page
    st.write("Already a User? [Login Here](#)")

    st.header("Welcome to our Marketing Page")
    st.write("This is your marketing content.")
    st.header("User Registration (Continuation)")

# Add more content for user registration (Continuation)
    st.write("This is the continuation of the User Registration page.")



def write_functions():
    st.sidebar.title("Navigation")
    st.write(editor_page())
    st.write(faq_data())
    st.write(for_groups())
    st.write(for_publisher())
    st.write(for_teaching())
    st.write(for_writing())
    st.write(premium_features())
    st.write(forgot_password())
    st.write(reset_password())
    st.write(home_page())
    st.write(home_page1())
    st.write(latex_editor())
    st.write(latex_history())
    st.write(payment_summary())
    st.write(pricing())
    st.write(user_plan())
    st.write(user_profile())
    st.write(register())
    st.write(dashboard())
    st.write(user_registration())


def main():

    selected_page = st.sidebar.radio("Go to", ["Editor Page", "FAQ DATA", "Groups", "Publisher", "Teaching", "Writing", "Premium Features", "Forgot Password", "Reset Password", "Home", "Home2", "Latex Editor", "Latex History", "Payment Summary", "Pricing", "User Plan", "User Profile", "Register", "Dashboard", "User Registration"])

    if selected_page == "Editor Page":
        editor_page()
    elif selected_page == "FAQ_DATA":
        faq_data()
    elif selected_page == "Groups":
        for_groups()
    elif selected_page == "Publisher":
        for_publisher()
    elif selected_page == "Teaching":
        for_teaching()
    elif selected_page == "Writing":
        for_writing()
    elif selected_page == "Premium Features":
        premium_features()
    elif selected_page == "Forgot Password":
        forgot_password()
    elif selected_page == "Reset Password":
        reset_password()
    elif selected_page == "Home":
        home_page()
    elif selected_page == "Home1":
        home_page1()
    elif selected_page == "Latex Editor":
        latex_editor()
    elif selected_page == "Latex History":
        latex_history()
    elif selected_page == "Payment Summary":
        payment_summary()
    elif selected_page == "Pricing":
        pricing()
    elif selected_page == "User Plan":
        user_plan()
    elif selected_page == "User Profile":
        user_profile()
    elif selected_page == "Register":
        register()
    elif selected_page =="Dashboard":
        dashboard()
    elif selected_page == "User Registration":
        user_registration()

    write_functions()

if __name__ == "__main__":
    main()