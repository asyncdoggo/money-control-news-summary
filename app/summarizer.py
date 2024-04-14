import os
from app.unlimiformer.usage import UnlimiformerArguments
os.environ['HF_HOME'] = os.path.join(os.getcwd(), 'hf_cache')
from app.unlimiformer.unlimiformer import Unlimiformer

from transformers import BartForConditionalGeneration, AutoTokenizer
import torch




class Summarizer:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        modelname = "abertsch/unlimiformer-bart-govreport-alternating"
        self.tokenizer = AutoTokenizer.from_pretrained("facebook/bart-base")
        model = BartForConditionalGeneration.from_pretrained(modelname)
        self.defaults = UnlimiformerArguments()
        self.unlimiformer_kwargs = {
                    'layer_begin': self.defaults.layer_begin, 
                    'layer_end': self.defaults.layer_end,
                    'unlimiformer_head_num': self.defaults.unlimiformer_head_num, 
                    'exclude_attention': self.defaults.unlimiformer_exclude, 
                    'chunk_overlap': self.defaults.unlimiformer_chunk_overlap,
                    'model_encoder_max_len': self.defaults.unlimiformer_chunk_size,
                    'verbose': self.defaults.unlimiformer_verbose, 'tokenizer': self.tokenizer,
                    'unlimiformer_training': self.defaults.unlimiformer_training,
                    'use_datastore': self.defaults.use_datastore,
                    'flat_index': self.defaults.flat_index,
                    'test_datastore': self.defaults.test_datastore,
                    'reconstruct_embeddings': self.defaults.reconstruct_embeddings,
                    'gpu_datastore': self.defaults.gpu_datastore,
                    'gpu_index': self.defaults.gpu_index
        }
        self.model = Unlimiformer.convert_model(model, **self.unlimiformer_kwargs)
        self.model.to(self.device)
        self.model.eval()

    def summarize(self, text, max_length=512):
        text_tokenized = self.tokenizer(text, truncation=False, return_tensors="pt")
        text_tokenized.to(self.device)
        summary_ids = self.model.generate(**text_tokenized, max_length=max_length)
        summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)

        del text_tokenized
        del summary_ids

        summary = summary.replace("GAO", "We")
        return summary
    


if __name__ == "__main__":
    summarizer = Summarizer()
    really_long_text = """
    Market movements may appear to be random in the short term, but there is a higher chance of markets delivering negative returns in the month of March than in any other month. If you look at monthly returns over the past 23 years, March saw negative returns 56 percent of the time, the highest of all months. This is not a random statistic. Experts suggest three reasons that explain this movement.Cash is kingA number of corporates and big market players might not want to show exposure to riskier assets like equities in their balance sheets. Thus, they might want to liquidate their positions to show a higher cash position on the closing day of the year, March 31. Ashish Goel, Managing Partner and Chief Executive Officer of Investsavvy PMS said, ``Companies tend to liquidate their positions in equities, show profits in the year-end balance sheet, and take new positions in the new financial year.’’Story continues below AdvertisementRemove AdAdvance taxMarch 15 is the deadline for the payment of 100 percent of your advance tax for the year. Although tax payment does not get bunched up during the end of the year any more as companies pay through the year in quarterly instalments, both individuals and corporates end up paying any remaining amount during the last quarter. This too can cause stocks or mutual funds to be sold to raise cash.Profit / loss bookingIf someone is sitting on a high level of realized gains, and have long-term losses on their portfolio, they may want to book those losses so they can offset the same against long-term capital gains and lower their tax liability. Similarly, if they have already realized losses on the portfolio, they may want to book profits on their long-term holdings, and re-enter those positions at the start of the next fiscal year, with minimal price risk. Related stories Expect nickel and gas prices to be lower for longerMoneycontrol Pro Panorama | FAME II subsidy scheme, if extended, can turbo charge EV demand Experts, however, said that while the March effect is certainly one factor pulling down the markets, regulatory action by SEBI (Securities and Exchange Board of India) and RBI (Reserve Bank of India) is also making investors wary and moderating money flows into markets.On February 27, the mutual funds industry body AMFI (Association of Mutual Funds in India), issued a circular based on an email received from SEBI. It said that SEBI has advised that given the froth building up in small and midcap stocks, mutual funds should put in place policies to safeguard the investors in such schemes. AMFI has recommended various means, such as rebalancing portfolios to increase the weightage of largecap stocks, and moderating flows into small and midcap funds.Then again, on March 5, RBI barred JM Financial from giving loans against debentures and shares, including sanction and disbursal of loans against IPO shares, with immediate effect.Story continues below AdvertisementRemove AdDisclaimer: The views and investment tips expressed by experts on Moneycontrol.com are their own and not those of the website or its management. Moneycontrol.com advises users to check with certified experts before taking any investment decisions.
    """
    print(len(really_long_text))
    summarized_text = summarizer.summarize(really_long_text, max_length=len(really_long_text) // 3)
    print(summarized_text)
    print(len(summarized_text))