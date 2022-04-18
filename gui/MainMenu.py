from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from gui.WindowUtils import WindowUtils


class MainMenu(WindowUtils):
    def __init__(self, centralWidget, baseStack, ownStack, wrap):
        super(MainMenu, self).__init__(wrap)
        self._baseStack = baseStack

        # Main title {{
        _title = QLabel("Othello")
        _title.setFont(QFont('Courier', 18))

        # laying out
        title_layout = self.horizontal_menu_widget_layouter(_title)
        # }}

        # Train ML agent #

        # select file {{
        train_file_lb = QLabel("Filename", centralWidget)
        train_file_lb.setMinimumWidth(100)

        self.train_file_cb = self.init_combobox(["file1", "file2"], centralWidget)

        # layout
        train_file_lt = self.horizontal_menu_widget_layouter(train_file_lb, self.train_file_cb)
        # }}

        # learning strategy {{
        learn_strat_lb = QLabel("Learning strategy", centralWidget)
        learn_strat_lb.setMinimumWidth(100)

        self.learn_strat_cb = self.init_combobox(["Q-learning"], centralWidget)

        learn_strat_lt = self.horizontal_menu_widget_layouter(learn_strat_lb, self.learn_strat_cb)
        # }}

        # learning rate {{
        learn_rate_lb = QLabel("Learning rate", centralWidget)
        learn_rate_lb.setMinimumWidth(100)

        self.learn_rate_sl = QSlider(Qt.Horizontal, centralWidget)
        self.learn_rate_sl.setMinimumWidth(125)
        self.learn_rate_sl.setMinimum(0)
        self.learn_rate_sl.setMaximum(100)
        self.learn_rate_sl.setTickInterval(5)

        learn_rate_lt = self.horizontal_menu_widget_layouter(learn_rate_lb, self.learn_rate_sl)
        # }}

        # random factor (epsilon) {{
        train_eps_lb = QLabel("Random factor", centralWidget)
        self.train_eps_sl = QSlider(Qt.Horizontal, centralWidget)
        self.train_eps_sl.setMinimumWidth(125)
        self.train_eps_sl.setMinimum(0)
        self.train_eps_sl.setMaximum(100)
        self.train_eps_sl.setTickInterval(5)

        train_eps_lt = self.horizontal_menu_widget_layouter(train_eps_lb, self.train_eps_sl)
        # }}

        # decrease random factor {{
        esp_dec_lb = QLabel("EPS decrease", centralWidget)
        self.esp_dec_sl = QSlider(Qt.Horizontal, centralWidget)
        self.esp_dec_sl.setMinimumWidth(125)
        self.esp_dec_sl.setMinimum(0)
        self.esp_dec_sl.setMaximum(100)
        self.esp_dec_sl.setTickInterval(5)

        esp_dec_lt = self.horizontal_menu_widget_layouter(esp_dec_lb, self.esp_dec_sl)
        # }}

        # ? lambda for TD ?

        # activation function {{
        act_fun_lb = QLabel("Activation function", centralWidget)
        act_fun_lb.setMinimumWidth(100)

        self.act_fun_cb = self.init_combobox(["sigmoïd", "ReLU", "hyperbolic tangent"], centralWidget)

        act_fun_lt = self.horizontal_menu_widget_layouter(act_fun_lb, self.act_fun_cb)
        # }}

        # number of games {{
        nb_trains_lb = QLabel("Number of games", centralWidget)
        nb_trains_lb.setMinimumWidth(100)

        self.nb_trains_sb = QSpinBox(centralWidget)
        self.nb_trains_sb.setMinimumWidth(125)
        self.nb_trains_sb.setRange(10000, 1000000)
        self.nb_trains_sb.setSingleStep(1000)

        nb_trains_lt = self.horizontal_menu_widget_layouter(nb_trains_lb, self.nb_trains_sb)
        # }}

        # launch button {{
        launch_train_btn = QPushButton("Train", centralWidget)
        launch_train_btn.setMinimumWidth(250)

        # connect
        launch_train_btn.clicked.connect(lambda: self.launch_training())

        launch_train_lt = self.horizontal_menu_widget_layouter(launch_train_btn)
        # }}

        # end Train ML agent #

        # Game against program #

        # choose type opponent AI {{
        opp_ai_lb = QLabel("Opponent AI", centralWidget)
        opp_ai_lb.setMinimumWidth(100)

        self.opp_ai_cb = self.init_combobox(["random", "ML agent", "minimax"], centralWidget)

        # layout
        opp_ai_lt = self.horizontal_menu_widget_layouter(opp_ai_lb, self.opp_ai_cb)
        # }}

        # minimax subtitle {{
        mnx_subtitle = QLabel("minimax")
        mnx_subtitle.setFont(QFont('Courier', 12))

        # laying out
        mnx_subtitle_lt = self.horizontal_menu_widget_layouter(mnx_subtitle)
        # }}

        # minimax early hits {{
        mnx_hits_lb = QLabel("Early hits")
        mnx_hits_lb.setMinimumWidth(100)

        self.mnx_hits_sb = QSpinBox(centralWidget)
        self.mnx_hits_sb.setMinimumWidth(125)
        self.mnx_hits_sb.setRange(0, 60)
        self.mnx_hits_sb.setSingleStep(1)

        # layout
        mnx_hits_lt = self.horizontal_menu_widget_layouter(mnx_hits_lb, self.mnx_hits_sb)
        # }}

        # ML agent subtitle {{
        ml_subtitle = QLabel("ML agent")
        ml_subtitle.setFont(QFont('Courier', 12))

        # laying out
        ml_subtitle_lt = self.horizontal_menu_widget_layouter(ml_subtitle)
        # }}

        # ML match file {{
        match_file_lb = QLabel("Filename", centralWidget)
        match_file_lb.setMinimumWidth(100)

        self.match_file_cb = self.init_combobox(["dummy fname 1", "dummy fname 2"], centralWidget)

        # layout
        match_file_lt = self.horizontal_menu_widget_layouter(match_file_lb, self.match_file_cb)
        # }}

        # random factor (epsilon) {{
        match_eps_lb = QLabel("Random factor", centralWidget)
        self.match_eps_sl = QSlider(Qt.Horizontal, centralWidget)
        self.match_eps_sl.setMinimumWidth(125)
        self.match_eps_sl.setMinimum(0)
        self.match_eps_sl.setMaximum(100)
        self.match_eps_sl.setTickInterval(5)

        # layout
        match_eps_lt = self.horizontal_menu_widget_layouter(match_eps_lb, self.match_eps_sl)
        # }}

        # TODO player chooses role?

        # launch button {{
        launch_match_btn = QPushButton("Play", centralWidget)
        launch_match_btn.setMinimumWidth(250)

        # connect
        launch_match_btn.clicked.connect(lambda: self.launch_match(baseStack, 1))

        launch_match_lt = self.horizontal_menu_widget_layouter(launch_match_btn)
        # }}

        # End of game against program #

        # New ML agent #

        # filename {{
        new_agent_fname_lb, self.new_agent_fname = self.label_and_input("Filename", centralWidget)

        new_agent_fname_lt = self.horizontal_menu_widget_layouter(new_agent_fname_lb, self.new_agent_fname)
        # }}

        # NN size {{
        nn_size_lb = QLabel("NN size")
        nn_size_lb.setMinimumWidth(100)

        self.nn_size_sb = QSpinBox(centralWidget)
        self.nn_size_sb.setMinimumWidth(125)
        self.nn_size_sb.setRange(1, 100)
        self.nn_size_sb.setSingleStep(1)

        # layout
        nn_size_lt = self.horizontal_menu_widget_layouter(nn_size_lb, self.nn_size_sb)
        # }}

        # TODO several layers?

        # Reward rule {{
        rw_rule_lb = QLabel("Reward rule", centralWidget)
        self.rw_rule_cb = self.init_combobox(["Victory", "Average pawns"], centralWidget)

        rw_rule_lt = self.horizontal_menu_widget_layouter(rw_rule_lb, self.rw_rule_cb)
        # }}

        # create button {{
        create_agent_btn = QPushButton("Create", centralWidget)
        create_agent_btn.setMinimumWidth(250)

        # connect
        create_agent_btn.clicked.connect(lambda: self.create_new_agent())

        create_agent_lt = self.horizontal_menu_widget_layouter(create_agent_btn)
        # }}
        # End new ML agent #

        # Comparison #

        # agent 1 subtitle {{
        agent1_subtitle = QLabel("Agent 1")
        agent1_subtitle.setFont(QFont('Courier', 12))

        # laying out
        agent1_subtitle_lt = self.horizontal_menu_widget_layouter(agent1_subtitle)
        # }}

        # agent 1 type {{
        agent1_type_lb = QLabel("Type", centralWidget)
        agent1_type_lb.setMinimumWidth(100)
        
        self.agent1_type_cb = self.init_combobox(["random", "ML agent", "minimax"], centralWidget)
        
        agent1_type_lt = self.horizontal_menu_widget_layouter(agent1_type_lb, self.agent1_type_cb)
        # }}

        # agent 1 file (ML) {{
        agent1_file_lb = QLabel("Filename (ML)", centralWidget)
        agent1_file_lb.setMinimumWidth(100)

        self.agent1_file_cb = self.init_combobox(["file1", "file2"], centralWidget)

        # layout
        agent1_file_lt = self.horizontal_menu_widget_layouter(agent1_file_lb, self.agent1_file_cb)
        # }}

        # random factor (epsilon) {{
        agent1_eps_lb = QLabel("Random factor (ML)", centralWidget)
        agent1_eps_lb.setMinimumWidth(100)
        self.agent1_eps_sl = QSlider(Qt.Horizontal, centralWidget)
        self.agent1_eps_sl.setMinimumWidth(125)
        self.agent1_eps_sl.setMinimum(0)
        self.agent1_eps_sl.setMaximum(100)
        self.agent1_eps_sl.setTickInterval(5)

        agent1_eps_lt = self.horizontal_menu_widget_layouter(agent1_eps_lb, self.agent1_eps_sl)
        # }}

        # agent 2 subtitle {{
        agent2_subtitle = QLabel("Agent 2")
        agent2_subtitle.setFont(QFont('Courier', 12))

        # laying out
        agent2_subtitle_lt = self.horizontal_menu_widget_layouter(agent2_subtitle)
        # }}

        # agent 2 type {{
        agent2_type_lb = QLabel("Type", centralWidget)
        agent2_type_lb.setMinimumWidth(100)
        
        self.agent2_type_cb = self.init_combobox(["random", "ML agent", "minimax"], centralWidget)
        
        agent2_type_lt = self.horizontal_menu_widget_layouter(agent2_type_lb, self.agent2_type_cb)
        # }}

        # agent 2 file (ML) {{
        agent2_file_lb = QLabel("Filename (ML)", centralWidget)
        agent2_file_lb.setMinimumWidth(100)

        self.agent2_file_cb = self.init_combobox(["file2", "file2"], centralWidget)

        # layout
        agent2_file_lt = self.horizontal_menu_widget_layouter(agent2_file_lb, self.agent2_file_cb)
        # }}

        # random factor (epsilon) {{
        agent2_eps_lb = QLabel("Random factor (ML)", centralWidget)
        agent2_eps_lb.setMinimumWidth(100)
        self.agent2_eps_sl = QSlider(Qt.Horizontal, centralWidget)
        self.agent2_eps_sl.setMinimumWidth(125)
        self.agent2_eps_sl.setMinimum(0)
        self.agent2_eps_sl.setMaximum(100)
        self.agent2_eps_sl.setTickInterval(5)

        agent2_eps_lt = self.horizontal_menu_widget_layouter(agent2_eps_lb, self.agent2_eps_sl)
        # }}

        # number of games {{
        nb_comps_lb = QLabel("Number of games", centralWidget)
        nb_comps_lb.setMinimumWidth(100)

        self.nb_comps_sb = QSpinBox(centralWidget)
        self.nb_comps_sb.setMinimumWidth(125)
        self.nb_comps_sb.setRange(10000, 1000000)
        self.nb_comps_sb.setSingleStep(1000)

        nb_comps_lt = self.horizontal_menu_widget_layouter(nb_comps_lb, self.nb_comps_sb)
        # }}

        # launch comparison button {{
        launch_comp_btn = QPushButton("Compare", centralWidget)
        launch_comp_btn.setMinimumWidth(250)

        # connect
        launch_comp_btn.clicked.connect(lambda: self.launch_comparison())

        launch_comp_lt = self.horizontal_menu_widget_layouter(launch_comp_btn)
        # }}

        # End comparison #

        # Groupboxes

        train_ml_gb = self.groupboxer("Train ML agent", train_file_lt, learn_strat_lt, learn_rate_lt, train_eps_lt,
                                      esp_dec_lt, act_fun_lt, nb_trains_lt, launch_train_lt)

        match_gb = self.groupboxer("Fight AI", opp_ai_lt, mnx_subtitle_lt, mnx_hits_lt, ml_subtitle_lt, match_file_lt,
                                   match_eps_lt, launch_match_lt)

        new_ml_gb = self.groupboxer("New ML agent", new_agent_fname_lt, nn_size_lt, rw_rule_lt, create_agent_lt)

        cmp_gb = self.groupboxer("Compare AIs", agent1_subtitle_lt, agent1_type_lt, agent1_file_lt, agent1_eps_lt,
                                 agent2_subtitle_lt, agent2_type_lt, agent2_file_lt, agent2_eps_lt, nb_comps_lt,
                                 launch_comp_lt)

        # finalize (layout the boxes)
        left_col = QVBoxLayout()
        left_col.addLayout(train_ml_gb)

        middle_col = QVBoxLayout()
        middle_col.addStretch()
        middle_col.addLayout(title_layout)
        middle_col.addStretch()
        middle_col.addLayout(match_gb)
        middle_col.addLayout(new_ml_gb)

        right_col = QVBoxLayout()
        right_col.addLayout(cmp_gb)

        mainmenu_layout = QHBoxLayout()
        mainmenu_layout.addLayout(left_col)
        mainmenu_layout.addLayout(middle_col)
        mainmenu_layout.addLayout(right_col)

        ownStack.setLayout(mainmenu_layout)

        # {{ end of __init__ }}

    def launch_training(self):
        print("Launch training requested")

    def launch_match(self, stack, menu_index):
        opp_type = self.opp_ai_cb.currentText()
        if opp_type == "random":
            print("fighting random agent")
        elif opp_type == "ML agent":
            print("fighting deepmind")
        else:
            print("fighting deepblue")

        stack.setCurrentIndex(menu_index)

    def create_new_agent(self):
        print("Create new agent requested")

    def launch_comparison(self):
        print("Launch comparison requested")
