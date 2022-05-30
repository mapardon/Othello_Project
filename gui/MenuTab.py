from PyQt5.QtCore import QThread
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from db.NNstorage import available_networks, save_new_network
from game.GameEngine import GameEngine
from gui.WindowUtils import WindowUtils


class MenuTab(WindowUtils):
    """ Defines UI elements for configuration menu """

    def __init__(self, centralWidget, baseStack, ownStack, wrap):
        """ Widgets declaration and connection to methods """

        super(MenuTab, self).__init__(wrap)
        self.baseStack = baseStack  # Allows menu navigation

        # Main title {{
        title = QLabel("Othello")
        title.setFont(QFont('Courier', 18))

        # laying out
        title_layout = QHBoxLayout()
        title_layout.addStretch()
        title_layout.addWidget(title)
        title_layout.addStretch()
        # }}

        # Train ML agent #

        # select file {{
        train_file_lb = QLabel("Filename", centralWidget)
        train_file_lb.setMinimumWidth(100)

        self.train_file_cb = self.init_combobox(list(), centralWidget)

        # layout
        train_file_lt = self.horizontal_menu_widget_layout(train_file_lb, self.train_file_cb)
        # }}

        # move selection {{
        move_selec_lb = QLabel("Move selection", centralWidget)
        move_selec_lb.setMinimumWidth(100)

        self.move_selec_cb = self.init_combobox(["eps-greedy", "softmax exponential"], centralWidget)

        self.move_selec_lt = self.horizontal_menu_widget_layout(move_selec_lb, self.move_selec_cb)
        # }}

        # learning rate {{
        learn_rate_lb = QLabel("Learning rate", centralWidget)
        learn_rate_lb.setMinimumWidth(100)

        self.learn_rate_sb = QDoubleSpinBox(centralWidget)
        self.learn_rate_sb.setMinimumWidth(125)
        self.learn_rate_sb.setRange(0, 1)
        self.learn_rate_sb.setSingleStep(0.05)

        learn_rate_lt = self.horizontal_menu_widget_layout(learn_rate_lb, self.learn_rate_sb)
        # }}

        # random factor (epsilon) {{
        train_eps_lb = QLabel("Random factor", centralWidget)
        train_eps_lb.setMinimumWidth(100)

        self.train_eps_sb = QDoubleSpinBox(centralWidget)
        self.train_eps_sb.setMinimumWidth(125)
        self.train_eps_sb.setRange(0, 1)
        self.train_eps_sb.setSingleStep(0.05)

        train_eps_lt = self.horizontal_menu_widget_layout(train_eps_lb, self.train_eps_sb)
        # }}

        # number of games {{
        nb_trains_lb = QLabel("Number of games", centralWidget)
        nb_trains_lb.setMinimumWidth(100)

        self.nb_trains_sb = QSpinBox(centralWidget)
        self.nb_trains_sb.setMinimumWidth(125)
        self.nb_trains_sb.setRange(1000, 1000000)
        self.nb_trains_sb.setSingleStep(1000)

        nb_trains_lt = self.horizontal_menu_widget_layout(nb_trains_lb, self.nb_trains_sb)
        # }}

        # progress bar {{
        train_prog_lb = QLabel("Training", centralWidget)
        train_prog_lb.setMinimumWidth(100)

        self.train_prog_pb = QProgressBar()
        self.train_prog_pb.setMinimumWidth(125)

        train_prog_lt = self.horizontal_menu_widget_layout(train_prog_lb, self.train_prog_pb)
        # }}

        # launch button {{
        self.launch_train_btn = QPushButton("Train", centralWidget)
        self.launch_train_btn.setMinimumWidth(250)

        # connect
        self.launch_train_btn.clicked.connect(lambda: self.launch_train_compare("train"))

        launch_train_lt = self.horizontal_menu_widget_layout(self.launch_train_btn)
        # }}
        # end Train ML agent #


        # Game against program #

        # player 1 type {{
        player_1_lb = QLabel("Player 1", centralWidget)
        player_1_lb.setMinimumWidth(100)

        self.player1_type_cb = self.init_combobox(["human", "random", "ML agent", "minimax"], centralWidget)

        # layout
        player1_lt = self.horizontal_menu_widget_layout(player_1_lb, self.player1_type_cb)
        # }}

        # player 2 type {{
        player_2_lb = QLabel("Player 2", centralWidget)
        player_2_lb.setMinimumWidth(100)

        self.player2_type_cb = self.init_combobox(["human", "random", "ML agent", "minimax"], centralWidget)

        # layout
        player2_lt = self.horizontal_menu_widget_layout(player_2_lb, self.player2_type_cb)
        # }}

        # pawns style {{
        pawns_style_lb = QLabel("Pawns style", centralWidget)
        pawns_style_lb.setMinimumWidth(100)

        self.pawns_style_cb = self.init_combobox(["classic", "undertale"], centralWidget)

        pawns_style_lt = self.horizontal_menu_widget_layout(pawns_style_lb, self.pawns_style_cb)
        # }}

        # random factor (epsilon) {{
        match_eps_lb = QLabel("Random factor", centralWidget)
        self.match_eps_sb = QDoubleSpinBox(centralWidget)
        self.match_eps_sb.setMinimumWidth(125)
        self.match_eps_sb.setRange(0, 1)
        self.match_eps_sb.setSingleStep(0.05)

        # layout
        match_eps_lt = self.horizontal_menu_widget_layout(match_eps_lb, self.match_eps_sb)
        # }}

        # ML agent subtitle {{
        ml_subtitle = QLabel("ML agent", centralWidget)
        ml_subtitle.setFont(QFont('Courier', 12))

        # laying out
        ml_subtitle_lt = self.horizontal_menu_widget_layout(ml_subtitle)
        # }}

        # ML match file (player 1) {{
        match_file1_lb = QLabel("Filename (agent 1)", centralWidget)
        match_file1_lb.setMinimumWidth(100)

        self.match_file1_cb = self.init_combobox(list(), centralWidget)

        # layout
        match_file1_lt = self.horizontal_menu_widget_layout(match_file1_lb, self.match_file1_cb)
        # }}

        # ML match file (player 2) {{
        match_file2_lb = QLabel("Filename (agent 2)", centralWidget)
        match_file2_lb.setMinimumWidth(100)

        self.match_file2_cb = self.init_combobox(list(), centralWidget)

        # layout
        match_file2_lt = self.horizontal_menu_widget_layout(match_file2_lb, self.match_file2_cb)
        # }}

        # minimax subtitle {{
        mnx_subtitle = QLabel("Minimax agent", centralWidget)
        mnx_subtitle.setFont(QFont('Courier', 12))

        # laying out
        mnx_subtitle_lt = self.horizontal_menu_widget_layout(mnx_subtitle)
        # }}

        # minimax early hits (player 1) {{
        play_ehits1_lb = QLabel("Depth (agent 1)")
        play_ehits1_lb.setMinimumWidth(100)

        self.play_ehits1_sb = QSpinBox(centralWidget)
        self.play_ehits1_sb.setMinimumWidth(125)
        self.play_ehits1_sb.setRange(0, 60)
        self.play_ehits1_sb.setSingleStep(1)

        # layout
        play_ehits1_lt = self.horizontal_menu_widget_layout(play_ehits1_lb, self.play_ehits1_sb)
        # }}

        # minimax early hits (player 2) {{
        play_ehits2_lb = QLabel("Depth (agent 2)")
        play_ehits2_lb.setMinimumWidth(100)

        self.play_ehits2_sb = QSpinBox(centralWidget)
        self.play_ehits2_sb.setMinimumWidth(125)
        self.play_ehits2_sb.setRange(0, 60)
        self.play_ehits2_sb.setSingleStep(1)

        # layout
        play_ehits2_lt = self.horizontal_menu_widget_layout(play_ehits2_lb, self.play_ehits2_sb)
        # }}

        # launch button {{
        self.launch_match_btn = QPushButton("Play", centralWidget)
        self.launch_match_btn.setMinimumWidth(250)

        # connect
        self.launch_match_btn.clicked.connect(lambda: self.launch_match(baseStack, 1))

        launch_match_lt = self.horizontal_menu_widget_layout(self.launch_match_btn)
        # }}

        # End of game against program #

        # New ML agent #

        # filename {{
        new_agent_fname_lb, self.new_agent_fname = self.label_and_input("Filename", centralWidget)

        new_agent_fname_lt = self.horizontal_menu_widget_layout(new_agent_fname_lb, self.new_agent_fname)
        # }}

        # NN size {{
        nn_size_lb = QLabel("NN size")
        nn_size_lb.setMinimumWidth(100)

        self.nn_size_sb = QSpinBox(centralWidget)
        self.nn_size_sb.setMinimumWidth(125)
        self.nn_size_sb.setRange(1, 100)
        self.nn_size_sb.setSingleStep(1)

        # layout
        nn_size_lt = self.horizontal_menu_widget_layout(nn_size_lb, self.nn_size_sb)
        # }}

        # learning strategy {{
        learn_strat_lb = QLabel("Learning strategy", centralWidget)
        learn_strat_lb.setMinimumWidth(100)

        self.learn_strat_cb = self.init_combobox(["Q-learning", "SARSA"], centralWidget)

        learn_strat_lt = self.horizontal_menu_widget_layout(learn_strat_lb, self.learn_strat_cb)
        # }}

        # activation function {{
        act_fun_lb = QLabel("Activation function", centralWidget)
        act_fun_lb.setMinimumWidth(100)

        self.act_fun_cb = self.init_combobox(["sigmoïd", "ReLU", "hyperbolic tangent"], centralWidget)

        act_fun_lt = self.horizontal_menu_widget_layout(act_fun_lb, self.act_fun_cb)
        # }}

        # create button {{
        self.create_agent_btn = QPushButton("Create", centralWidget)
        self.create_agent_btn.setMinimumWidth(250)

        # connect
        self.create_agent_btn.clicked.connect(lambda: self.create_new_agent())

        create_agent_lt = self.horizontal_menu_widget_layout(self.create_agent_btn)
        # }}
        # End new ML agent #

        # Comparison #

        # agent 1 type {{
        agent1_type_lb = QLabel("Agent 1", centralWidget)
        agent1_type_lb.setMinimumWidth(100)

        self.agent1_type_cb = self.init_combobox(["random", "ML agent", "minimax"], centralWidget)

        agent1_type_lt = self.horizontal_menu_widget_layout(agent1_type_lb, self.agent1_type_cb)
        # }}

        # agent 2 type {{
        agent2_type_lb = QLabel("Agent 2", centralWidget)
        agent2_type_lb.setMinimumWidth(100)

        self.agent2_type_cb = self.init_combobox(["random", "ML agent", "minimax"], centralWidget)

        agent2_type_lt = self.horizontal_menu_widget_layout(agent2_type_lb, self.agent2_type_cb)
        # }}

        # number of games {{
        nb_comps_lb = QLabel("Number of games", centralWidget)
        nb_comps_lb.setMinimumWidth(100)

        self.nb_comps_sb = QSpinBox(centralWidget)
        self.nb_comps_sb.setMinimumWidth(125)
        self.nb_comps_sb.setRange(1, 1000000)
        self.nb_comps_sb.setSingleStep(1000)

        nb_comps_lt = self.horizontal_menu_widget_layout(nb_comps_lb, self.nb_comps_sb)
        # }}

        # random factor (epsilon) {{
        cmp_eps_lb = QLabel("Random factor", centralWidget)
        cmp_eps_lb.setMinimumWidth(100)
        self.cmp_eps_sb = QDoubleSpinBox(centralWidget)
        self.cmp_eps_sb.setMinimumWidth(125)
        self.cmp_eps_sb.setRange(0, 1)
        self.cmp_eps_sb.setSingleStep(0.05)

        cmp_eps_lt = self.horizontal_menu_widget_layout(cmp_eps_lb, self.cmp_eps_sb)
        # }}

        # ML agent subtitle {{
        cmp_ml_agent_subtitle = QLabel("ML agent")
        cmp_ml_agent_subtitle.setFont(QFont('Courier', 12))

        # laying out
        cmp_ml_agent_subtitle_lt = self.horizontal_menu_widget_layout(cmp_ml_agent_subtitle)
        # }}

        # agent 1 file (ML) {{
        agent1_file_lb = QLabel("Filename (ML)", centralWidget)
        agent1_file_lb.setMinimumWidth(100)

        self.agent1_file_cb = self.init_combobox(list(), centralWidget)

        # layout
        agent1_file_lt = self.horizontal_menu_widget_layout(agent1_file_lb, self.agent1_file_cb)
        # }}

        # agent 2 file (ML) {{
        agent2_file_lb = QLabel("Filename (ML)", centralWidget)
        agent2_file_lb.setMinimumWidth(100)

        self.agent2_file_cb = self.init_combobox(list(), centralWidget)

        # layout
        agent2_file_lt = self.horizontal_menu_widget_layout(agent2_file_lb, self.agent2_file_cb)
        # }}

        # minimax agent subtitle {{
        cmp_minimax_agent_subtitle = QLabel("Minimax agent")
        cmp_minimax_agent_subtitle.setFont(QFont('Courier', 12))

        # laying out
        cmp_minimax_agent_subtitle_lt = self.horizontal_menu_widget_layout(cmp_minimax_agent_subtitle)
        # }}

        # minimax early hits (agent 1) {{
        cmp_ehits1_lb = QLabel("Depth (agent 1)")
        cmp_ehits1_lb.setMinimumWidth(100)

        self.cmp_ehits1_sb = QSpinBox(centralWidget)
        self.cmp_ehits1_sb.setMinimumWidth(125)
        self.cmp_ehits1_sb.setRange(0, 60)
        self.cmp_ehits1_sb.setSingleStep(1)

        # layout
        cmp_ehits1_lt = self.horizontal_menu_widget_layout(cmp_ehits1_lb, self.cmp_ehits1_sb)
        # }}

        # minimax early hits (agent 2) {{
        cmp_ehits2_lb = QLabel("Depth (agent 2)")
        cmp_ehits2_lb.setMinimumWidth(100)

        self.cmp_ehits2_sb = QSpinBox(centralWidget)
        self.cmp_ehits2_sb.setMinimumWidth(125)
        self.cmp_ehits2_sb.setRange(0, 60)
        self.cmp_ehits2_sb.setSingleStep(1)

        # layout
        cmp_ehits2_lt = self.horizontal_menu_widget_layout(cmp_ehits2_lb, self.cmp_ehits2_sb)
        # }}

        # progress bar {{
        cmp_prog_lb = QLabel("Training", centralWidget)
        cmp_prog_lb.setMinimumWidth(100)

        self.cmp_prog_pb = QProgressBar()
        self.cmp_prog_pb.setMinimumWidth(125)

        cmp_prog_lt = self.horizontal_menu_widget_layout(cmp_prog_lb, self.cmp_prog_pb)
        # }}

        # results {{
        results_w_lb = QLabel("Results:", centralWidget)
        results_w_lb.setMinimumWidth(100)

        self.results_w_dsp = QLabel(str(), centralWidget)
        self.results_w_dsp.setMinimumWidth(100)

        results_b_lb = QLabel(str(), centralWidget)
        results_b_lb.setMinimumWidth(100)

        self.results_b_dsp = QLabel(str(), centralWidget)
        self.results_b_dsp.setMinimumWidth(100)

        results_t_lb = QLabel(str(), centralWidget)
        results_t_lb.setMinimumWidth(100)

        self.results_t_dsp = QLabel(str(), centralWidget)
        self.results_t_dsp.setMinimumWidth(100)

        cmp_results_lt = QVBoxLayout()
        cmp_results_lt.addLayout(self.horizontal_menu_widget_layout(results_b_lb, self.results_b_dsp))
        cmp_results_lt.addLayout(self.horizontal_menu_widget_layout(results_w_lb, self.results_w_dsp))
        cmp_results_lt.addLayout(self.horizontal_menu_widget_layout(results_t_lb, self.results_t_dsp))
        # }}

        # launch comparison button {{
        self.launch_comp_btn = QPushButton("Compare", centralWidget)
        self.launch_comp_btn.setMinimumWidth(250)

        # connect
        self.launch_comp_btn.clicked.connect(lambda: self.launch_train_compare("compare"))

        launch_comp_lt = self.horizontal_menu_widget_layout(self.launch_comp_btn)
        # }}

        # End comparison #

        self.update_comboboxes()

        # Groupboxes
        train_ml_gb = self.groupboxer("Train ML agent", train_file_lt, self.move_selec_lt, learn_rate_lt, train_eps_lt,
                                      nb_trains_lt, train_prog_lt, launch_train_lt)

        match_gb = self.groupboxer("Match", player1_lt, player2_lt, pawns_style_lt, match_eps_lt, ml_subtitle_lt,
                                   match_file1_lt, match_file2_lt, mnx_subtitle_lt, play_ehits1_lt, play_ehits2_lt,
                                   launch_match_lt)

        new_ml_gb = self.groupboxer("New ML agent", new_agent_fname_lt, nn_size_lt, learn_strat_lt, act_fun_lt,
                                    create_agent_lt)

        cmp_gb = self.groupboxer("Compare AIs", agent1_type_lt, agent2_type_lt, nb_comps_lt, cmp_eps_lt,
                                 cmp_ml_agent_subtitle_lt, agent1_file_lt, agent2_file_lt,
                                 cmp_minimax_agent_subtitle_lt, cmp_ehits1_lt, cmp_ehits2_lt, cmp_prog_lt,
                                 cmp_results_lt, launch_comp_lt)

        # finalize (layout the boxes)
        left_col = QVBoxLayout()
        left_col.addWidget(match_gb)

        middle_col = QVBoxLayout()
        middle_col.addStretch()
        middle_col.addLayout(title_layout)
        middle_col.addStretch()
        middle_col.addWidget(train_ml_gb)
        middle_col.addWidget(new_ml_gb)

        right_col = QVBoxLayout()
        right_col.addWidget(cmp_gb)

        mainmenu_layout = QHBoxLayout()
        mainmenu_layout.addLayout(left_col)
        mainmenu_layout.addLayout(middle_col)
        mainmenu_layout.addLayout(right_col)

        ownStack.setLayout(mainmenu_layout)

        # {{ end of __init__ }}

    # Utility functions #
    def fetch_parameters(self, game_mode):
        """ Read parameters from the widgets. All cases (match, train, comapre) are handled independently since
        parameters are provided by different widgets for those cases. """

        game_parameters = dict()

        if game_mode == "match":
            self.wrap.pawns_style = self.pawns_style_cb.currentText()
            game_parameters = {"mode": "match",
                               "player1": {"type": self.player1_type_cb.currentText().lower()},
                               "player2": {"type": self.player2_type_cb.currentText().lower()},
                               "nb_games": None}
            pars = None
            if game_parameters["player1"]["type"] == "ml agent":
                pars = {"network_name": self.match_file1_cb.currentText(), "eps": self.match_eps_sb.value()}
            elif game_parameters["player1"]["type"] == "minimax":
                pars = {"ehits": self.play_ehits1_sb.value(), "eps": self.match_eps_sb.value()}
            game_parameters["player1"]["pars"] = pars

            pars = None
            if game_parameters["player2"]["type"] == "ml agent":
                pars = {"network_name": self.match_file2_cb.currentText(), "eps": self.cmp_eps_sb.value()}
            elif game_parameters["player2"]["type"] == "minimax":
                pars = {"ehits": self.play_ehits2_sb.value(), "eps": self.cmp_eps_sb.value()}
            game_parameters["player2"]["pars"] = pars

        elif game_mode == "train":
            game_parameters = {"mode": "train",
                               "player1": {"type": "ml agent",
                                           "pars": {"network_name": self.train_file_cb.currentText(),
                                                    "eps": self.train_eps_sb.value(), "ls": None,
                                                    "mv_selec": self.move_selec_cb.currentText().split(" ")[0],
                                                    "lr": self.learn_rate_sb.value(), "act_f": None}},
                               "player2": None,
                               "nb_games": self.nb_trains_sb.value()}

        elif game_mode == "compare":
            game_parameters = {"mode": "compare",
                               "player1": {"type": self.agent1_type_cb.currentText().lower()},
                               "player2": {"type": self.agent2_type_cb.currentText().lower()},
                               "nb_games": self.nb_comps_sb.value()}
            pars = None
            if game_parameters["player1"]["type"] == "ml agent":
                pars = {"network_name": self.agent1_file_cb.currentText(), "eps": self.cmp_eps_sb.value()}
            elif game_parameters["player1"]["type"] == "minimax":
                pars = {"ehits": self.cmp_ehits1_sb.value(), "eps": self.cmp_eps_sb.value()}
            game_parameters["player1"]["pars"] = pars

            pars = None
            if game_parameters["player2"]["type"] == "ml agent":
                pars = {"network_name": self.agent2_file_cb.currentText(), "eps": self.cmp_eps_sb.value()}
            elif game_parameters["player2"]["type"] == "minimax":
                pars = {"ehits": self.cmp_ehits2_sb.value(), "eps": self.cmp_eps_sb.value()}
            game_parameters["player2"]["pars"] = pars

        return game_parameters

    def toggle_buttons_activation(self):
        disabling = self.launch_match_btn.isEnabled()
        self.launch_match_btn.setDisabled(disabling)
        self.create_agent_btn.setDisabled(disabling)
        self.launch_comp_btn.setDisabled(disabling)
        self.launch_train_btn.setDisabled(disabling)

    def update_comboboxes(self):
        """ Update contents of comboboxes that may be influenced by UI """
        for cb in [self.match_file1_cb, self.match_file2_cb, self.agent1_file_cb, self.agent2_file_cb, self.train_file_cb]:
            cb.clear()
            for f in available_networks():
                cb.addItem(f)
            if cb.count():
                cb.setCurrentIndex(0)

    # Button triggered operations #

    def create_new_agent(self):
        network_name = self.new_agent_fname.text()
        if network_name in available_networks():
            self.informative_popup("Warning", "Archived ai with this filename already exists.", "dismiss")

        elif network_name == str():
            self.informative_popup("Warning", "Filename must not be empty.", "dismiss")

        else:
            save_new_network(network_name, self.learn_strat_cb.currentText(), self.act_fun_cb.currentText().lower(), 128, self.nn_size_sb.value())
            self.update_comboboxes()
        self.new_agent_fname.setText(str())

    def launch_match(self, stack, menu_index):
        self.wrap.game_parameters = self.fetch_parameters("match")
        stack.setCurrentIndex(menu_index)

    def display_results(self, results):
        """ Display results after comparison session """

        self.results_w_dsp.setText(results[0])
        self.results_b_dsp.setText(results[1])
        self.results_t_dsp.setText(results[2])

    def launch_train_compare(self, mode):
        """ Launch train or compare loop in QThread. Same function is used for both purposes since GameEngine is passed
        parameter indicating if it's dealing with training or comparison. """

        self.toggle_buttons_activation()

        # Initialization of the QThread object
        self.thread = QThread()
        self.worker = GameEngine(self, self.fetch_parameters(mode))
        self.worker.moveToThread(self.thread)

        # Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.toggle_buttons_activation)

        # Other signals & slots
        self.worker.train_progress.connect(self.train_prog_pb.setValue)
        self.worker.compare_progress.connect(self.cmp_prog_pb.setValue)
        self.worker.compare_result.connect(self.display_results)

        # Start the thread
        self.thread.start()
