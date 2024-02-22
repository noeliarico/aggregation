ggplot(mallow1_condorcet %>%
         filter(dispersion %in% c(0.1, 0.4, 0.7, 1),
                num_voters %in% c(10, 50, 100, 200, 500, 1000)
         ) %>%
         mutate(dispersion = as.factor(dispersion)), aes(dispersion, fill = type)) +
  facet_grid(num_alternatives~num_voters,
             labeller = custom_labeller) +
  geom_bar(color = "black") +
  geom_text(stat = "count", aes(label = ifelse(stat(count) > 10, stat(count), "")),
            position = position_stack(vjust = 0.5), color = "black",
            size = theme_get()$text$size/(18/5),
            family = theme_get()$text$family) +
  scale_fill_manual(values = palCondorcet) +
  labs(x = "Diversidad",
       y = "Total",
       fill = "Tipo de perfil") +
  guides(fill=guide_legend(nrow=1,ncol=3,byrow=TRUE,label.position ="left")) +
  theme(panel.grid.major.x = element_blank(),
        panel.grid.minor.x = element_blank(),
        panel.grid.major.y = element_blank(),
        panel.grid.minor.y = element_blank(),
        axis.text.x = element_text(angle = 0, vjust = 0.5, hjust = 0.5),
        axis.ticks.y = element_blank(),
        axis.text.y = element_blank())


ggsave(filename = "~/Desktop/fig_tfg_miguel/fig_mallow1_distribuciones_Condorcet.pdf",
       height = 15, width = 18, units = "cm", dpi = 300)
